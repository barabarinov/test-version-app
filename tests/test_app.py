from http import HTTPStatus


class TestStatusEndpoint:
    """Tests for GET /status endpoint"""

    def test_get_status_no_version(self, no_version_state):
        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.NOT_FOUND
        assert version is None

    def test_get_status_version_1(self, version_1_state):
        status_code, version = version_1_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1"

    def test_get_status_version_1_1(self, version_1_1_state):
        status_code, version = version_1_1_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1.1"

    def test_get_status_version_2(self, version_2_state):
        status_code, version = version_2_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "2"


class TestSetStatusEndpoint:
    """Tests for POST /setStatus endpoint"""

    def test_set_status_when_no_version(self, no_version_state):
        status_code = no_version_state.set_status()
        assert status_code == HTTPStatus.CREATED

        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1"

    def test_set_status_when_version_exists(self, version_1_state):
        status_code = version_1_state.set_status()
        assert status_code == HTTPStatus.BAD_REQUEST

        status_code, version = version_1_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1"


class TestUpdateStatusEndpoint:
    """Tests for PATCH /updateStatus endpoint"""

    def test_update_status_no_version(self, no_version_state):
        status_code = no_version_state.update_status()
        assert status_code == HTTPStatus.BAD_REQUEST

        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.NOT_FOUND
        assert version is None

    def test_update_status_from_version_1(self, version_1_state):
        status_code = version_1_state.update_status()
        assert status_code == HTTPStatus.OK

        status_code, version = version_1_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1.1"

    def test_update_status_from_version_1_1(self, version_1_1_state):
        status_code = version_1_1_state.update_status()
        assert status_code == HTTPStatus.OK

        status_code, version = version_1_1_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1.2"

    def test_update_status_from_version_2(self, version_2_state):
        status_code = version_2_state.update_status()
        assert status_code == HTTPStatus.OK

        status_code, version = version_2_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "2.1"


class TestRewriteStatusEndpoint:
    """Tests for PUT /rewriteStatus endpoint"""

    def test_rewrite_status_no_version(self, no_version_state):
        status_code = no_version_state.rewrite_status()
        assert status_code == HTTPStatus.BAD_REQUEST

        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.NOT_FOUND
        assert version is None

    def test_rewrite_status_from_version_1(self, version_1_state):
        status_code = version_1_state.rewrite_status()
        assert status_code == HTTPStatus.OK

        status_code, versione = version_1_state.get_status()
        assert status_code == HTTPStatus.OK
        assert versione == "2"

    def test_rewrite_status_from_version_1_1(self, version_1_1_state):
        status_code = version_1_1_state.rewrite_status()
        assert status_code == HTTPStatus.OK

        status_code, version = version_1_1_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "2"


class TestRemoveStatusEndpoint:
    """Tests for DELETE /removeStatus endpoint"""

    def test_remove_status_no_version(self, no_version_state):
        status_code = no_version_state.remove_status()
        assert status_code == HTTPStatus.OK

        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.NOT_FOUND
        assert version is None

    def test_remove_status_from_version_1(self, version_1_state):
        status_code = version_1_state.remove_status()
        assert status_code == HTTPStatus.OK

        status_code, version = version_1_state.get_status()
        assert status_code == HTTPStatus.NOT_FOUND
        assert version is None

    def test_remove_status_from_version_2(self, version_2_state):
        status_code = version_2_state.remove_status()
        assert status_code == HTTPStatus.OK

        status_code, version = version_2_state.get_status()
        assert status_code == HTTPStatus.NOT_FOUND
        assert version is None


class TestRollbackStatusEndpoint:
    """Tests for POST /rollbackStatusVersion endpoint"""

    def test_rollback_status_no_version(self, no_version_state):
        status_code = no_version_state.rollback_status()
        assert status_code == HTTPStatus.BAD_REQUEST

        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.NOT_FOUND
        assert version is None

    def test_rollback_status_from_version_1(self, version_1_state):
        status_code = version_1_state.rollback_status()
        assert status_code == HTTPStatus.BAD_REQUEST

        status_code, version = version_1_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1"

    def test_rollback_status_from_version_2(self, version_2_state):
        status_code = version_2_state.rollback_status()
        assert status_code == HTTPStatus.OK

        status_code, version = version_2_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1"

    def test_rollback_to_specific_version(self, version_2_state):
        status_code = version_2_state.rollback_status("1.1")
        assert status_code == HTTPStatus.OK

        status_code, version = version_2_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1.1"

    def test_rollback_to_invalid_version(self, version_2_state):
        status_code = version_2_state.rollback_status("5")
        assert status_code == HTTPStatus.BAD_REQUEST

        status_code, version = version_2_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "2"


class TestStateTransitions:
    """Tests for complex state transitions"""

    def test_full_version_lifecycle(self, no_version_state):
        # Start with no version
        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.NOT_FOUND
        assert version is None

        # Set initial version
        status_code = no_version_state.set_status()
        assert status_code == HTTPStatus.CREATED

        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1"

        # Update to minor version
        status_code = no_version_state.update_status()
        assert status_code == HTTPStatus.OK

        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1.1"

        # Update to another minor version
        status_code = no_version_state.update_status()
        assert status_code == HTTPStatus.OK

        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1.2"

        # Rewrite to major version
        status_code = no_version_state.rewrite_status()
        assert status_code == HTTPStatus.OK

        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "2"

        # Rollback to previous major
        status_code = no_version_state.rollback_status()
        assert status_code == HTTPStatus.OK

        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1"

        # Remove status
        status_code = no_version_state.remove_status()
        assert status_code == HTTPStatus.OK

        status_code, version = no_version_state.get_status()
        assert status_code == HTTPStatus.NOT_FOUND
        assert version is None

    def test_multiple_minor_updates(self, version_1_state):
        expected_versions = ["1.1", "1.2", "1.3"]
        for expected_version in expected_versions:
            status_code = version_1_state.update_status()
            assert status_code == HTTPStatus.OK

            status_code, version = version_1_state.get_status()
            assert status_code == HTTPStatus.OK
            assert version == expected_version


class TestEdgeCases:
    """Tests for edge cases and error conditions"""

    def test_invalid_rollback_version_format(self, version_2_state):
        status_code = version_2_state.rollback_status("invalid")
        assert status_code == HTTPStatus.BAD_REQUEST

        status_code, version = version_2_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "2"

    def test_rollback_with_empty_body(self, version_2_state):
        status_code = version_2_state.rollback_status()
        assert status_code == HTTPStatus.OK

        status_code, version = version_2_state.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1"

    def test_consecutive_major_version_updates(self, version_1_state):
        expected_versions = ["2", "3", "4"]
        for expected_version in expected_versions:
            status_code = version_1_state.rewrite_status()
            assert status_code == HTTPStatus.OK

            status_code, version = version_1_state.get_status()
            assert status_code == HTTPStatus.OK
            assert version == expected_version

    def test_multiple_operations_sequence(self, clean_state, api_client):
        # Set initial version
        status_code = api_client.set_status()
        assert status_code == HTTPStatus.CREATED

        status_code, version = api_client.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1"

        # Multiple minor updates
        for expected_minor in range(1, 4):
            status_code = api_client.update_status()
            assert status_code == HTTPStatus.OK

            status_code, version = api_client.get_status()
            assert status_code == HTTPStatus.OK
            assert version == f"1.{expected_minor}"

        # Major update
        status_code = api_client.rewrite_status()
        assert status_code == HTTPStatus.OK

        status_code, version = api_client.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "2"

        # More minor updates on new major version
        status_code = api_client.update_status()
        assert status_code == HTTPStatus.OK

        status_code, version = api_client.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "2.1"

        # Rollback to specific version
        status_code = api_client.rollback_status("1.2")
        assert status_code == HTTPStatus.OK

        status_code, version = api_client.get_status()
        assert status_code == HTTPStatus.OK
        assert version == "1.2"
