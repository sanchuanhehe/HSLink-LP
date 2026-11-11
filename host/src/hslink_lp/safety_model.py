"""Executable control-policy reference; no GPIO, firmware or HID transport.

Timing values must come from hardware qualification. Tests supply synthetic values;
a completed timer means a sequencing guard elapsed, never a measured voltage.
"""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Timing:
    relay_release: float
    mos_off: float
    vio_start: float

    def __post_init__(self):
        if any(not math.isfinite(v) or v <= 0 for v in vars(self).values()):
            raise ValueError("qualification timing must be finite and positive")


@dataclass
class SafetyModel:
    timing: Timing
    now: float = 0.0
    measurement_locked: bool = True
    usb_valid: bool = False
    signals: bool = False
    sense: bool = False
    power: bool = False
    discharge: bool = False
    vio_en: bool = False
    vio_ready: bool = False
    vio_setpoint: float | None = None
    generation: int = 0
    vio_deadline: float | None = None
    pending_power: float | None = None
    pending_discharge: tuple[float, float] | None = None
    discharge_deadline: float | None = None
    power_off_since: float = 0.0
    last_discharge_result: str = "not_requested"

    def isolate(self):
        self.signals = self.sense = False

    def reset(self):
        self.generation += 1
        self.isolate()
        self.measurement_locked = True
        self.power = self.discharge = self.vio_en = self.vio_ready = False
        self.vio_setpoint = None
        self.vio_deadline = self.pending_power = None
        self.pending_discharge = self.discharge_deadline = None
        self.power_off_since = self.now
        self.last_discharge_result = "aborted_voltage_unknown"

    def usb(self, valid: bool):
        # Both loss and recovery enter a fresh, disconnected state.
        self.reset()
        self.usb_valid = valid

    def enter_measurement(self):
        self.isolate()
        self.measurement_locked = True
        self.cancel_discharge()
        self.pending_power = None
        # An already energized relay may remain energized.

    def exit_measurement(self):
        if not self.usb_valid:
            raise ValueError("USB not valid")
        self.measurement_locked = False
        # Explicit unlock alone does not reconnect anything.

    def set_vio(self, volts: float) -> int:
        if not self.usb_valid or not math.isfinite(volts) or not 1.8 <= volts <= 3.3:
            raise ValueError("invalid VIO request")
        self.isolate()
        self.vio_en = self.vio_ready = False
        self.vio_deadline = None
        self.generation += 1
        self.vio_setpoint = volts
        return self.generation

    def dac_configured(self, token: int, *, readback_ok: bool, calibration_valid: bool):
        # Readback confirms digital configuration only, not measured VIO.
        if token != self.generation or not self.usb_valid or self.vio_setpoint is None:
            return False
        self.isolate()
        if not readback_ok or not calibration_valid:
            self.vio_en = self.vio_ready = False
            self.vio_deadline = None
            return False
        self.vio_en = True
        self.vio_ready = False
        self.vio_deadline = self.now + self.timing.vio_start
        return True

    def connect_signals(self, *, target_voltage_match_confirmed: bool):
        if (self.measurement_locked or not self.usb_valid or not self.vio_ready
                or not target_voltage_match_confirmed or self.discharge
                or self.pending_discharge is not None):
            raise ValueError("connection not permitted")
        self.signals = True

    def request_vref(self):
        if self.measurement_locked or not self.usb_valid or self.discharge or self.pending_discharge:
            raise ValueError("Vref unavailable while isolated")
        self.sense = True

    def cancel_discharge(self):
        if self.discharge or self.pending_discharge is not None:
            self.last_discharge_result = "cancelled_voltage_unknown"
        self.discharge = False
        self.pending_discharge = self.discharge_deadline = None

    def power_off(self):
        self.isolate()
        self.power = False
        self.pending_power = None
        self.cancel_discharge()
        self.power_off_since = self.now

    def power_on(self):
        if not self.usb_valid:
            raise ValueError("USB not valid")
        self.cancel_discharge()
        # Stale DISCH_REQ cannot resume when POWER_SAFE changes again.
        self.pending_power = self.now + self.timing.mos_off

    def request_discharge(self, duration: float):
        if self.measurement_locked or not self.usb_valid:
            raise ValueError("discharge not permitted")
        if not math.isfinite(duration) or not 0 < duration <= 10:
            raise ValueError("finite bounded prototype discharge required")
        self.power_off()
        self.pending_discharge = (self.now + self.timing.relay_release, duration)
        self.last_discharge_result = "requested_voltage_unknown"

    def unrelated_command(self, command: str):
        if command not in {"uart_open", "dtr", "rts", "dap"}:
            raise ValueError(command)
        # No implicit state transition is permitted by the policy.

    def tick(self, now: float):
        if not math.isfinite(now) or now < self.now:
            raise ValueError("monotonic clock required")
        self.now = now
        if not self.usb_valid:
            return
        if self.vio_deadline is not None and now >= self.vio_deadline:
            self.vio_ready = True
            self.vio_deadline = None
        if self.pending_power is not None and now >= self.pending_power:
            self.cancel_discharge()
            self.power = True
            self.pending_power = None
        if self.pending_discharge is not None:
            start, duration = self.pending_discharge
            if now >= start:
                self.pending_discharge = None
                # A delayed scheduler must not extend an expired discharge pulse.
                if now < start + duration:
                    self.discharge = True
                    self.discharge_deadline = start + duration
                else:
                    self.last_discharge_result = "timer_elapsed_voltage_unknown"
        if self.discharge_deadline is not None and now >= self.discharge_deadline:
            self.discharge = False
            self.discharge_deadline = None
            self.last_discharge_result = "timer_elapsed_voltage_unknown"

    def assert_invariants(self):
        assert not (self.power and self.discharge)
        if self.measurement_locked:
            assert not (self.signals or self.sense or self.discharge or self.pending_discharge)
        if not self.usb_valid:
            assert not (self.power or self.discharge or self.signals or self.sense or self.vio_en)
        if self.signals:
            assert self.vio_en and self.vio_ready
        if self.discharge:
            assert self.now >= self.power_off_since + self.timing.relay_release
