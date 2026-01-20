def resolve_results(results: list) -> dict:
    if not results:
        return {
            "final_status": "FAIL",
            "confidence": 0.0,
            "failed_checks": []
        }
    
    failed = [r for r in results if not r["status"]]
    confidence = 1 - (len(failed) / len(results))

    return {
        "final_status": "PASS" if len(failed) == 0 else "FAIL",
        "confidence": round(confidence, 2),
        "failed_checks": failed
    }
