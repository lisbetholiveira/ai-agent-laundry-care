import re
from dataclasses import asdict

from .models import ColorAnalysis, FabricAnalysis, StainAnalysis


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


class Guardrails:
    """Basic request validation before the specialist workflow runs."""

    def validate(self, user_input: str) -> tuple[bool, str]:
        if not user_input or not user_input.strip():
            return False, "Please describe the garment or laundry-care problem."
        if len(user_input) > 1500:
            return False, "Please shorten the request so it can be processed clearly."
        return True, ""


class LaundryRequestClassifier:
    """Route only laundry/clothing-care requests into the specialist workflow."""

    KEYWORDS = {
        "wash", "washing", "laundry", "dry", "dryer", "drying", "iron", "ironing",
        "stain", "fabric", "clothes", "clothing", "garment", "shirt", "jumper",
        "sweater", "dress", "jeans", "denim", "wool", "cotton", "silk",
        "polyester", "linen", "cashmere", "nylon", "acrylic", "rayon", "lace",
        "coffee", "wine", "grease", "sweat", "ink", "blood", "bleach", "detergent"
    }

    def classify(self, user_input: str) -> bool:
        text = _normalise(user_input)
        return any(keyword in text for keyword in self.KEYWORDS)


class FabricAgent:
    """Classify fabric and return conservative care constraints."""

    GROUPS = {
        "cotton": ("cotton", "linen", "denim", "canvas"),
        "wool": ("wool", "cashmere", "knit", "fleece"),
        "silk": ("silk", "satin", "lace", "rayon"),
        "synthetic": ("polyester", "nylon", "spandex", "acrylic"),
    }

    def analyse(self, user_input: str) -> FabricAnalysis:
        text = _normalise(user_input)
        fabric = "unknown"

        for group, keywords in self.GROUPS.items():
            if any(keyword in text for keyword in keywords):
                fabric = group
                break

        delicate_markers = ("wool", "cashmere", "silk", "satin", "lace", "rayon", "sequin", "embellish")
        is_delicate = any(marker in text for marker in delicate_markers)

        if fabric == "wool":
            return FabricAnalysis(
                fabric="wool",
                is_delicate=True,
                temperature="cold",
                programme="wool or delicate cycle",
                spin="low spin",
                notes=["Avoid aggressive rubbing.", "Check the garment care label."],
            )
        if fabric == "silk":
            return FabricAnalysis(
                fabric="silk/delicate",
                is_delicate=True,
                temperature="cold",
                programme="delicate cycle or hand wash if the label requires it",
                spin="very low spin or no spin",
                notes=["Use gentle handling.", "Check the garment care label."],
            )
        if fabric == "synthetic":
            return FabricAnalysis(
                fabric="synthetic",
                is_delicate=False,
                temperature="cool",
                programme="synthetics or gentle cycle",
                spin="medium spin",
                notes=["Check the garment care label."],
            )
        if fabric == "cotton":
            return FabricAnalysis(
                fabric="cotton/linen/denim",
                is_delicate=False,
                temperature="cool to warm, subject to the care label",
                programme="normal or appropriate fabric cycle",
                spin="medium spin",
                notes=["Check the garment care label before using higher temperatures."],
            )

        return FabricAnalysis(
            fabric="unknown",
            is_delicate=is_delicate,
            temperature="cold or cool",
            programme="gentle cycle",
            spin="low spin",
            notes=["Fabric could not be identified confidently.", "Check the garment care label."],
        )


class ColorAgent:
    """Assess separation, temperature preference and bleach risk."""

    def analyse(self, user_input: str, fabric: FabricAnalysis) -> ColorAnalysis:
        text = _normalise(user_input)

        if any(word in text for word in ("white", "whites")):
            color_group = "white"
        elif any(word in text for word in ("black", "dark", "navy")):
            color_group = "dark"
        elif any(word in text for word in ("red", "bright", "vivid")):
            color_group = "bright"
        elif any(word in text for word in ("light", "pastel", "beige", "cream")):
            color_group = "light"
        else:
            color_group = "unknown"

        separate = color_group in {"white", "dark", "bright"}
        prefer_low_temperature = fabric.is_delicate or color_group in {"dark", "bright", "unknown"}
        avoid_bleach = fabric.is_delicate or color_group != "white"

        notes: list[str] = []
        if color_group == "white":
            notes.append("Wash separately from dark or strongly coloured items.")
        elif color_group == "dark":
            notes.append("Wash with similar dark colours.")
        elif color_group == "bright":
            notes.append("Wash with similar colours and use a low temperature.")
        elif color_group == "unknown":
            notes.append("Colour was not identified; use a cautious, low-temperature approach.")

        if fabric.is_delicate:
            notes.append("Avoid bleach because the fabric is delicate.")

        return ColorAnalysis(
            color_group=color_group,
            separate=separate,
            prefer_low_temperature=prefer_low_temperature,
            avoid_bleach=avoid_bleach,
            notes=notes,
        )


class StainAgent:
    """Identify a supported stain and return a conservative pre-treatment step."""

    STAIN_TYPES = ("wine", "grease", "sweat", "ink", "coffee", "blood")

    def analyse(self, user_input: str, fabric: FabricAnalysis) -> StainAnalysis:
        text = _normalise(user_input)
        stain = next((item for item in self.STAIN_TYPES if item in text), "unknown")

        if stain == "wine":
            return StainAnalysis(
                stain="wine",
                pretreatment="Gently pre-treat with cold water and a mild detergent.",
                avoid=["heat", "aggressive rubbing"],
            )
        if stain == "blood":
            return StainAnalysis(
                stain="blood",
                pretreatment="Rinse or blot with cold water before washing.",
                avoid=["hot water", "heat before the stain is removed"],
            )
        if stain == "grease":
            return StainAnalysis(
                stain="grease",
                pretreatment="Apply a small amount of mild liquid detergent to the stain before washing.",
                avoid=["machine drying before confirming the stain is gone"],
            )
        if stain == "coffee":
            return StainAnalysis(
                stain="coffee",
                pretreatment="Blot and rinse with cool water, then use a mild detergent.",
                avoid=["heat before the stain is removed"],
            )
        if stain == "ink":
            return StainAnalysis(
                stain="ink",
                pretreatment="Blot gently and use a fabric-compatible stain treatment only if the care label allows it.",
                avoid=["aggressive rubbing"],
            )
        if stain == "sweat":
            return StainAnalysis(
                stain="sweat",
                pretreatment="Pre-treat gently with a mild detergent before washing.",
                avoid=["strong bleach on delicate fabrics"],
            )

        if "stain" in text:
            return StainAnalysis(
                stain="unknown",
                pretreatment="Blot gently and use cold or cool water until the stain type is identified.",
                avoid=["heat", "aggressive rubbing"],
            )

        return StainAnalysis(stain="none identified", pretreatment="No stain-specific pre-treatment identified.", avoid=[])


class ClarificationAgent:
    def respond(self) -> str:
        return (
            "I can help with laundry and clothing-care questions such as washing, drying, "
            "ironing, stains, fabrics and colour care. Please reformulate your request within that scope."
        )


class FinalInstructionAgent:
    """Combine specialist outputs into one user-facing recommendation."""

    def synthesise(
        self,
        fabric: FabricAnalysis,
        color: ColorAnalysis,
        stain: StainAnalysis,
    ) -> str:
        parts = [
            f"Recommended approach: use {fabric.temperature} water and a {fabric.programme}, with {fabric.spin}."
        ]

        if stain.stain != "none identified":
            parts.append(stain.pretreatment)

        if color.separate:
            if color.color_group == "white":
                parts.append("Wash the garment separately from dark or strongly coloured items.")
            else:
                parts.append(f"Wash with similar {color.color_group} colours.")

        avoid_items = list(stain.avoid)
        if color.avoid_bleach and "bleach" not in avoid_items:
            avoid_items.append("bleach")
        if fabric.is_delicate and "high spin" not in avoid_items:
            avoid_items.append("high spin")

        if avoid_items:
            parts.append("Avoid " + ", ".join(avoid_items) + ".")

        parts.append("Always check the garment care label before washing.")
        return " ".join(parts)


def serialise_analysis(value):
    return asdict(value)
