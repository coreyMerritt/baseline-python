from services.value_objects.full_health_report import FullHealthReport


class HealthManager:
  def get_full_health_report(self) -> FullHealthReport:
    # TODO
    return FullHealthReport(
      healthy=True
    )
