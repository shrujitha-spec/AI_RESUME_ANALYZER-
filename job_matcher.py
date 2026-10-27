
import re


def _norm(text):
    text = str(text).lower()
    text = re.sub(r"[-_/]", " ", text)
    text = re.sub(r"[^a-z0-9+#. ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def match_roles(resume_text, roles_df):
    text = " " + _norm(resume_text) + " "
    scores = []
    for skills in roles_df["required_skills"]:
        required = [_norm(s) for s in str(skills).split(",") if s.strip()]
        found = sum(1 for r in required if " " + r + " " in text or " " + r + "s " in text)
        scores.append(100 * found / len(required) if required else 0)
    result = roles_df.copy()
    result["score"] = scores
    return result.sort_values("score", ascending=False).reset_index(drop=True)
