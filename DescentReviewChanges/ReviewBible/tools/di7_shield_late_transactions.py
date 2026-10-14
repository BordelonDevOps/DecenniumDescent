"""Current Shield evaluator after actual GPT DI7-SHIELD-LATE-01.

The original ShieldTransactions/report remain preserved as pre-ruling history.
This extension closes negative admission across applications of the ward family.
It does not grant an intervening action window or implement incoming schedulers.
"""
from di7_shield_transactions import ShieldTransactions


class ShieldLateTransactions(ShieldTransactions):
    def admit(self, oid, component_id, target, *, positive_pre_share=False):
        occurrence, component = self._component(oid, component_id)
        allowed = component['preShareTargets'] if positive_pre_share else component['directTargets']
        if target not in allowed:
            raise ValueError('Actual final recipient/source-qualified share required')
        if target in occurrence['noClaimAtFirst']:
            # Family admission is closed, even if a same/new application is now
            # available. The existing claim path remains bound to its exact old
            # application; termination/replacement never transfers that claim.
            return None
        return super().admit(oid, component_id, target, positive_pre_share=positive_pre_share)
