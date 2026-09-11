"""Arabic language utilities.

Handles Arabic language processing, normalization, and dialect support.
"""

import re
from typing import Optional


class ArabicNormalizer:
    """Arabic text normalization."""

    # Arabic normalization mappings
    ALEF_VARIANTS = {"ا": "ا", "أ": "ا", "إ": "ا", "آ": "ا"}
    HA_VARIANTS = {"ة": "ه", "ه": "ه"}

    @staticmethod
    def normalize(text: str) -> str:
        """Normalize Arabic text.

        Args:
            text: Arabic text to normalize

        Returns:
            Normalized text
        """
        # Normalize alef variants
        for variant, normalized in ArabicNormalizer.ALEF_VARIANTS.items():
            text = text.replace(variant, normalized)

        # Normalize ha variants
        for variant, normalized in ArabicNormalizer.HA_VARIANTS.items():
            text = text.replace(variant, normalized)

        # Remove diacritics
        text = re.sub(r"[\u064B-\u0652]", "", text)

        return text.strip()

    @staticmethod
    def is_arabic(text: str) -> bool:
        """Check if text contains Arabic.

        Args:
            text: Text to check

        Returns:
            True if text contains Arabic
        """
        arabic_pattern = r"[\u0600-\u06FF]"
        return bool(re.search(arabic_pattern, text))


class ArabicDialectHandler:
    """Handle Egyptian and Modern Standard Arabic."""

    # Common Egyptian dialect to MSA mappings
    EGYPTIAN_TO_MSA = {
        "معايا": "معي",
        "عايز": "أريد",
        "فين": "أين",
        "ايه": "ما",
        "اتنين": "اثنان",
        "كام": "كم",
    }

    @staticmethod
    def to_msa(text: str) -> str:
        """Convert Egyptian dialect to Modern Standard Arabic.

        Args:
            text: Egyptian Arabic text

        Returns:
            MSA text
        """
        result = text
        for egyptian, msa in ArabicDialectHandler.EGYPTIAN_TO_MSA.items():
            result = result.replace(egyptian, msa)
        return result

    @staticmethod
    def identify_dialect(text: str) -> str:
        """Identify Arabic dialect.

        Args:
            text: Arabic text

        Returns:
            Dialect identifier: "egyptian", "msa", or "mixed"
        """
        egyptian_markers = [
            "معايا",
            "عايز",
            "فين",
            "ايه",
            "اتنين",
            "كام",
        ]
        egyptian_count = sum(1 for marker in egyptian_markers if marker in text)

        if egyptian_count > len(text.split()) * 0.2:  # >20% Egyptian words
            return "egyptian"
        return "msa"


class FinancialTerminologyArabic:
    """Arabic financial terminology support."""

    TERMS = {
        # Core terms
        "رأس المال": "capital",
        "الأسهم": "stocks",
        "السهم": "stock",
        "السعر": "price",
        "الربح": "profit",
        "الخسارة": "loss",
        "المحفظة": "portfolio",
        "التداول": "trading",
        "الاستثمار": "investment",
        "المخاطرة": "risk",
        # Market types
        "البورصة": "exchange",
        "السوق": "market",
        "العملات": "currencies",
        "السلع": "commodities",
        # Analysis
        "التحليل الأساسي": "fundamental analysis",
        "التحليل الفني": "technical analysis",
        "الاتجاه": "trend",
        "المتوسط المتحرك": "moving average",
        "الزخم": "momentum",
        # Risk terms
        "إدارة المخاطر": "risk management",
        "وقف الخسارة": "stop loss",
        "أخذ الربح": "take profit",
        "النسبة": "ratio",
        "التقلب": "volatility",
        # Economic
        "الفائدة": "interest",
        "التضخم": "inflation",
        "الناتج المحلي الإجمالي": "GDP",
        "البطالة": "unemployment",
    }

    @staticmethod
    def get_english(arabic_term: str) -> Optional[str]:
        """Get English term for Arabic financial term.

        Args:
            arabic_term: Arabic term

        Returns:
            English equivalent or None
        """
        return FinancialTerminologyArabic.TERMS.get(arabic_term)

    @staticmethod
    def get_arabic(english_term: str) -> Optional[str]:
        """Get Arabic term for English financial term.

        Args:
            english_term: English term

        Returns:
            Arabic equivalent or None
        """
        for arabic, english in FinancialTerminologyArabic.TERMS.items():
            if english.lower() == english_term.lower():
                return arabic
        return None


class ArabicFormatter:
    """Format numbers and currency in Arabic."""

    @staticmethod
    def format_currency(amount: float, currency: str = "EGP") -> str:
        """Format amount as currency.

        Args:
            amount: Amount to format
            currency: Currency code

        Returns:
            Formatted string in Arabic
        """
        # Arabic numerals
        arabic_numerals = "٠١٢٣٤٥٦٧٨٩"
        digits = "0123456789"

        formatted = f"{amount:,.2f}"
        # Convert to Arabic numerals
        for i, digit in enumerate(digits):
            formatted = formatted.replace(digit, arabic_numerals[i])

        currency_ar = {
            "EGP": "جنيه مصري",
            "USD": "دولار أمريكي",
            "EUR": "يورو",
            "GBP": "جنيه إسترليني",
        }.get(currency, currency)

        return f"{formatted} {currency_ar}"

    @staticmethod
    def format_percentage(value: float, decimals: int = 2) -> str:
        """Format percentage in Arabic.

        Args:
            value: Percentage value
            decimals: Decimal places

        Returns:
            Formatted percentage string
        """
        arabic_numerals = "٠١٢٣٤٥٦٧٨٩"
        digits = "0123456789"

        formatted = f"{value:.{decimals}f}%"
        for i, digit in enumerate(digits):
            formatted = formatted.replace(digit, arabic_numerals[i])

        return formatted
