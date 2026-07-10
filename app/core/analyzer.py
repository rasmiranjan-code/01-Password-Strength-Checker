"""
Password analysis coordinator.

This module orchestrates the entire password analysis workflow by
integrating the results from various core components:

- PasswordChecker: Validates password rules.
- PasswordScorer: Calculates a strength score.
- PasswordEntropy: Estimates entropy in bits.
- RecommendationEngine: Generates improvement tips.

The final, consolidated result is returned as a PasswordAnalysisResult
object, providing a comprehensive overview of the password's security.
"""

from __future__ import annotations

from app.core.checker import PasswordChecker
from app.core.entropy import PasswordEntropy
from app.core.recommendations import RecommendationEngine
from app.core.scorer import PasswordScorer
from app.models import PasswordAnalysisResult
from app.security import CrackTimeEstimator, PwnedPasswordChecker
from app.utils.logger import get_logger


logger = get_logger(__name__)


class PasswordAnalyzer:
    """
    Coordinates the password analysis process.
    """

    def __init__(self) -> None:
        self.checker = PasswordChecker()
        self.scorer = PasswordScorer()
        self.entropy_calculator = PasswordEntropy()
        self.recommendation_engine = RecommendationEngine()
        self.crack_time_estimator = CrackTimeEstimator()
        self.pwned_checker = PwnedPasswordChecker()
        logger.info("PasswordAnalyzer initialized with all components.")

    def analyze(self, password: str) -> PasswordAnalysisResult:
        """
        Perform a full analysis of the given password.

        Args:
            password: The password to analyze.

        Returns:
            A PasswordAnalysisResult object with the complete analysis.
        """
        analysis_result = PasswordAnalysisResult(password=password)

        try:
            # 1. Validate password rules
            validation_result = self.checker.check(password)
            analysis_result.validation = validation_result

            # 2. Calculate strength score
            score = self.scorer.calculate_score(validation_result)
            analysis_result.score = score
            analysis_result.strength = self.scorer.get_strength_label(score)

            # 3. Calculate entropy
            entropy = self.entropy_calculator.calculate_entropy(password)
            analysis_result.entropy = entropy
            analysis_result.entropy_level = (
                self.entropy_calculator.get_entropy_level(entropy)
            )

            # 4. Estimate crack time
            crack_time = self.crack_time_estimator.estimate_crack_time(entropy)
            analysis_result.estimated_crack_time = crack_time

            # 5. Check if password is pwned
            pwned_count = self.pwned_checker.check_password(password)
            analysis_result.pwned_count = pwned_count
            if pwned_count > 0:
                validation_result.is_pwned = True

            # 6. Generate recommendations
            recommendations = self.recommendation_engine.generate_recommendations(
                validation_result
            )
            analysis_result.recommendations = recommendations

            analysis_result.analysed_successfully = True
            logger.info("Password analysis completed successfully.")

        except Exception as e:
            logger.exception("An error occurred during password analysis: %s", e)
            analysis_result.analysed_successfully = False

        return analysis_result