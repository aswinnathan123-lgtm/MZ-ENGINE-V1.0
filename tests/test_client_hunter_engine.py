from core.client_hunter_engine import ClientHunterEngine


def test_niche_benchmarks_exposed_as_class_data():
    assert "Gym & Fitness Centers" in ClientHunterEngine.niche_benchmarks
    assert "Dental & Healthcare" in ClientHunterEngine.niche_benchmarks


def test_scan_locality_clients_returns_results():
    engine = ClientHunterEngine()
    data = engine.scan_locality_clients("Gym & Fitness Centers", "Madhanandhapuram")

    assert data["total_leads_found"] > 0
    assert len(data["leads"]) > 0
    assert data["leads"][0]["niche"] == "Gym & Fitness Centers"
