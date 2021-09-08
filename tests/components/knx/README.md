# Testing the KNX integration

A KNXTestKit instance can be requested from a fixture. It provides convenience methods
am was sent to `group_address`.
  The telegram will be removed from the assertion queue.
- `knx.assert_response(group_address: str, payload: int | tuple[int, ...])`
  Asserts that a GroupValueResponse telegram with `payload` was sent to `group_address`.
  The telegram will be removed from the assertion queue.
- `knx.assert_write(group_address: str, payload: int | tuple[int, ...])`
  Asserts that a GroupValueWrite telegram with `payload` was sent to `group_address`.
  The telegram will be removed from the assertion queue.

Change some states or call some services and assert outgoing telegrams.

```python
    # turn on switch
    await hass.services.async_call(
        "switch", "turn_on", {"entity_id": "switch.test_switch"}, blocking=True
    )
    # assert ON telegram
    await knx.assert_write("1/2/3", True)
```

## Injecting incoming telegrams

- `knx.receive_read(group_address: str)`
  Inject and process a GroupValueRead telegram addressed to `group_address`.
- `knx.receive_response(group_address: str, payload: int | tuple[int, ...])`
  Inject and process a GroupValueResponse telegram addressed to `group_address` containing `payload`.
- `knx.receive_write(group_address: str, payload: int | tuple[int, ...])`
  Inject and process a GroupValueWrite telegram addressed to `group_address` containing `payload`.

Receive some telegrams and assert state.

```python
    # receive OFF telegram
    await knx.receive_write("1/2/3", False)
    # assert OFF state
    state = hass.states.get("switch.test_switch")
    assert state.state is STATE_OFF
```

## Notes

- For `payload` in `assert_*` and `receive_*` use `int` for DPT 1, 2 and 3 payload values (DPTBinary) and `tuple` for other DPTs (DPTArray).
- `await self.hass.async_block_till_done()` is called before `KNXTestKit.assert_*` and after `KNXTestKit.receive_*` so you don't have to explicitly call it.
- Make sure to assert every outgoing telegram that was created in a test. `assert_no_telegram` is automatically called on teardown.
