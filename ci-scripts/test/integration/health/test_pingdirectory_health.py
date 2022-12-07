import requests

from health_common import Categories, TestHealthBase


class TestPingDirectoryHealth(TestHealthBase):
    job_name = "healthcheck-pingdirectory"
    pingdirectory = "pingDirectory"

    def test_pingdirectory_health_cron_job_exists(self):
        cron_jobs = self.batch_client.list_cron_job_for_all_namespaces()
        cron_job_name = next(
            (
                cron_job.metadata.name
                for cron_job in cron_jobs.items
                if cron_job.metadata.name == self.job_name
            ),
            "",
        )
        self.assertEqual(
            self.job_name,
            cron_job_name,
            f"Cron job '{self.job_name}' not found in cluster",
        )

    def test_health_check_has_pingdirectory_results(self):
        res = requests.get(self.endpoint, verify=False)
        self.assertIn(
            self.pingdirectory,
            res.json()["health"].keys(),
            f"No {self.pingdirectory} in health check results",
        )

    def test_health_check_has_replica_backlog_count_results(self):
        test_results = self.get_test_results(self.pingdirectory, Categories.pod_status)
        expected = "replica backlog count"
        self.assertIn(
            expected,
            test_results.keys(),
            f"No '{expected}' checks found in health check results",
        )

    def test_health_check_has_failed_replay_updated_results(self):
        test_results = self.get_test_results(self.pingdirectory, Categories.connectivity)
        expected = "failed replay updated"
        self.assertIn(
            expected,
            test_results.keys(),
            f"No '{expected}' checks found in health check results",
        )

    def test_health_check_has_unresolved_naming_conflicts_results(self):
        test_results = self.get_test_results(self.pingdirectory, Categories.pod_status)
        expected = "unresolved naming conflicts"
        self.assertIn(
            expected,
            test_results.keys(),
            f"No '{expected}' checks found in health check results",
        )
