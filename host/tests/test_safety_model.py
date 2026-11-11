import random
import unittest
from hslink_lp.safety_model import SafetyModel, Timing

# Synthetic test clocks; these are NOT approved hardware timing constants.
class SafetyPolicyTests(unittest.TestCase):
    def setUp(self):
        self.s = SafetyModel(Timing(0.05, 0.002, 0.005))
        self.s.usb(True)

    def ready(self):
        token = self.s.set_vio(1.8)
        self.assertTrue(self.s.dac_configured(token, readback_ok=True, calibration_valid=True))
        self.s.tick(self.s.now + 0.006)

    def test_measurement_lock_survives_adjustment_and_other_commands(self):
        self.s.power_on(); self.s.tick(0.003)
        self.ready()
        for command in ['uart_open', 'dtr', 'rts', 'dap']:
            self.s.unrelated_command(command)
        with self.assertRaises(ValueError): self.s.request_vref()
        with self.assertRaises(ValueError): self.s.connect_signals(target_voltage_match_confirmed=True)
        self.assertTrue(self.s.power)
        self.assertTrue(self.s.measurement_locked)
        self.s.assert_invariants()

    def test_reconnect_requires_explicit_request_after_settling(self):
        self.ready(); self.s.exit_measurement()
        self.assertFalse(self.s.signals)
        self.s.connect_signals(target_voltage_match_confirmed=True)
        token = self.s.set_vio(3.3)
        with self.assertRaises(ValueError): self.s.connect_signals(target_voltage_match_confirmed=True)
        self.s.dac_configured(token, readback_ok=True, calibration_valid=True)
        self.s.tick(self.s.now + 0.01)
        self.assertFalse(self.s.signals)
        with self.assertRaises(ValueError): self.s.connect_signals(target_voltage_match_confirmed=False)

    def test_stale_dac_completion_after_reset_or_new_request(self):
        token = self.s.set_vio(1.8)
        self.s.set_vio(3.3)
        self.assertFalse(self.s.dac_configured(token, readback_ok=True, calibration_valid=True))
        token = self.s.generation; self.s.reset()
        self.assertFalse(self.s.dac_configured(token, readback_ok=True, calibration_valid=True))
        self.s.assert_invariants()

    def test_bad_calibration_or_readback_never_enables(self):
        token = self.s.set_vio(1.8)
        for readback, calibration in [(False, True), (True, False)]:
            self.assertFalse(self.s.dac_configured(token, readback_ok=readback, calibration_valid=calibration))
            self.s.tick(self.s.now + 1)
            self.assertFalse(self.s.vio_en)

    def test_reset_during_discharge_cancels_pending_and_active(self):
        for delay in [0.01, 0.06]:
            self.s.exit_measurement(); self.s.request_discharge(1)
            self.s.tick(self.s.now + delay); self.s.reset(); self.s.tick(self.s.now + 2)
            self.assertFalse(self.s.discharge); self.s.assert_invariants()

    def test_power_restoration_clears_stale_discharge_request(self):
        self.s.exit_measurement(); self.s.request_discharge(1); self.s.tick(0.06)
        self.assertTrue(self.s.discharge)
        self.s.power_on(); self.assertFalse(self.s.discharge)
        self.s.tick(0.063); self.assertTrue(self.s.power)
        self.s.power_off(); self.s.tick(2)
        self.assertFalse(self.s.discharge)

    def test_usb_loss_recovery_no_automatic_rearm(self):
        self.s.exit_measurement(); self.s.request_discharge(1); self.s.tick(0.06)
        self.s.usb(False); self.s.tick(1); self.s.usb(True); self.s.tick(2)
        self.assertFalse(self.s.power or self.s.discharge or self.s.signals)
        self.assertTrue(self.s.measurement_locked)

    def test_timeout_does_not_claim_voltage_or_extend_pulse(self):
        self.s.exit_measurement(); self.s.request_discharge(0.1); self.s.tick(1)
        self.assertFalse(self.s.discharge)
        self.assertEqual(self.s.last_discharge_result, 'timer_elapsed_voltage_unknown')

    def test_measurement_entry_cancels_discharge_and_pending_power(self):
        self.s.exit_measurement(); self.s.request_discharge(1); self.s.enter_measurement()
        self.s.tick(2); self.s.assert_invariants()
        self.s.power_on(); self.s.enter_measurement(); self.s.tick(3)
        self.assertFalse(self.s.power)

    def test_configuration_failure_while_connected_isolates(self):
        self.ready(); self.s.exit_measurement()
        self.s.connect_signals(target_voltage_match_confirmed=True)
        self.s.dac_configured(self.s.generation, readback_ok=False, calibration_valid=True)
        self.assertFalse(self.s.signals or self.s.vio_en)
        self.s.assert_invariants()

    def test_invalid_numbers_rejected(self):
        for bad in [float('nan'), float('inf'), -1, 0]:
            with self.assertRaises(ValueError): Timing(bad, 1, 1)
            with self.assertRaises(ValueError): self.s.set_vio(bad)
        with self.assertRaises(ValueError): self.s.tick(float('nan'))

    def test_random_event_sequences_preserve_invariants(self):
        rng = random.Random(5301)
        events = [lambda:self.s.usb(False), lambda:self.s.usb(True), self.s.reset,
            self.s.enter_measurement, self.s.exit_measurement, self.s.power_on,
            self.s.power_off, lambda:self.s.request_discharge(0.1),
            lambda:self.s.tick(self.s.now + rng.choice([0.001,0.01,0.1])),
            lambda:self.s.set_vio(rng.choice([1.8,2.5,3.3])),
            lambda:self.s.dac_configured(self.s.generation, readback_ok=True, calibration_valid=True),
            self.s.request_vref, lambda:self.s.connect_signals(target_voltage_match_confirmed=True),
            lambda:self.s.unrelated_command('dap')]
        for _ in range(10000):
            try: rng.choice(events)()
            except ValueError: pass
            self.s.assert_invariants()

if __name__ == '__main__': unittest.main()
