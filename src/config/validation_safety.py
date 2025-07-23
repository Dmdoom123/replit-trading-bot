"""
Streamlined Validation Safety System
Only prevents critical zero values that would break the bot
"""

import logging
from typing import Dict, Any, Optional, Tuple

class ValidationSafety:
    """Simplified safety controls - only critical bot-breaking validations"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Only the most critical parameters that CANNOT be zero
        self.critical_zero_checks = {
            'margin': 50.0,
            'leverage': 5,
            'assessment_interval': 60
        }

    def validate_parameter(self, param_name: str, value: Any) -> Tuple[bool, Any, Optional[str]]:
        """
        Simplified validation - only check critical zero values
        Returns: (is_valid, corrected_value, error_message)
        """
        # Only validate critical parameters that cannot be zero
        if param_name not in self.critical_zero_checks:
            return True, value, None

        try:
            # Convert to appropriate type
            if param_name == 'leverage' or param_name == 'assessment_interval':
                value = int(value)
            else:
                value = float(value)
        except (ValueError, TypeError):
            default_value = self.critical_zero_checks[param_name]
            return False, default_value, f"Invalid value type for {param_name}"

        # Critical zero check only
        if value == 0:
            default_value = self.critical_zero_checks[param_name]
            error_msg = f"🚫 {param_name} cannot be zero - this would break the bot"
            self.logger.warning(f"CRITICAL SAFETY: {param_name} = 0 blocked, using {default_value}")
            return False, default_value, error_msg

        # No other validations - let user set any non-zero value
        return True, value, None

    def validate_strategy_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate complete strategy configuration - simplified safety checks
        Returns: True if config is safe, False if critical issues found
        """
        if not config:
            return False
            
        # Check critical zero values that would break the bot
        for param_name in self.critical_zero_checks:
            if param_name in config:
                is_valid, _, _ = self.validate_parameter(param_name, config[param_name])
                if not is_valid:
                    self.logger.error(f"🚫 CRITICAL: {param_name} validation failed in strategy config")
                    return False
        
        return True

    def validate_multiple_parameters(self, updates: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        Validate multiple parameters - simplified approach
        Returns: (validated_updates, error_messages)
        """
        validated_updates = {}
        error_messages = {}

        for param_name, value in updates.items():
            is_valid, corrected_value, error_msg = self.validate_parameter(param_name, value)

            validated_updates[param_name] = corrected_value
            if error_msg:
                error_messages[param_name] = error_msg
                self.logger.warning(f"🔧 SAFETY CORRECTION: {param_name} = {value} → {corrected_value}")

        return validated_updates, error_messages

# Global validation safety instance
validation_safety = ValidationSafety()