# coding:utf-8
import logging
import functools


logger = logging.getLogger(__name__)


OS_FAMILY = "ubuntu"
OS_VERSION = "14.04"


IMG_NAME = "api-test-image"
IMG_PLATFORM = "ec2"
IMG_LOCATION = "us-east-1"
IMG_ID = "ami-10b68a78"
IMG_ARCH = "x86_64"


ROLE_NAME = "api-test-role"
ROLE_CATEGORY = {"id": 1}



def find_os(session):
    logger.info("Querying for OS: '%s' : '%s'", OS_FAMILY, OS_VERSION)

    os_query = {"family": OS_FAMILY, "version": OS_VERSION}
    os_list = session.list("/api/user/v1/os/", params=os_query)
    assert len(os_list) == 1, "Filtering error: got {0} OS for query ({1})".format(len(os_list), os_query)

    return os_list[0]


def create_image(session, env_id, os):
    logger.info("Creating Image with OS: %s", os["id"])
    return session.create("/api/user/v1/{0}/images/".format(env_id), json={
        "name": IMG_NAME,
        "cloudImageId": IMG_ID,
        "cloudPlatform": IMG_PLATFORM,
        "cloudLocation": IMG_LOCATION,
        "architecture": IMG_ARCH,
        "os": os,
    })


def delete_image(session, env_id, image):
    logger.info("Deleting Image: %s", image["name"])
    session.delete("/api/user/v1/{0}/images/{1}/".format(env_id, image["id"]))


def create_role(session, env_id, os):
    logger.info("Creating Role with OS: %s", os["id"])
    return session.create("/api/user/v1/{0}/roles/".format(env_id), json={
        "name": ROLE_NAME,
        "category": ROLE_CATEGORY,
        "os": os,
    })


def delete_role(session, env_id, role):
    logger.info("Deleting Role: %s", role["name"])
    session.delete("/api/user/v1/{0}/roles/{1}/".format(env_id, role["id"]))


def associate_image_with_role(session, env_id, role, image):
    logger.info("Associating Image %s with Role %s", image["name"], role["name"])
    return session.create("/api/user/v1/{0}/roles/{1}/images/".format(env_id, role["id"]), json=image)


def disassociate_image_from_role(session, env_id, role, image):
    logger.info("Disassociating Image %s from Role %s", image["name"], role["name"])
    session.delete("/api/user/v1/{0}/roles/{1}/images/{2}/".format(env_id, role["id"], image["id"]))


def execute(session, env_id):
    cleanup_actions = []

    os = find_os(session)

    try:

        # Creation phase

        # Create Image, and schedule it for cleanup
        image = create_image(session, env_id, os)
        cleanup_actions.append(functools.partial(delete_image, session, env_id, image))

        # Create Role, and scheduling it for cleanup
        role = create_role(session, env_id, os)
        cleanup_actions.append(functools.partial(delete_role, session, env_id, role))

        # Associate Image with Role
        associate_image_with_role(session, env_id, role, image)
        cleanup_actions.append(functools.partial(disassociate_image_from_role, session, env_id, role, image))

    finally:
        # TODO - Report:
        # - REPORTED - Possible to delete Image without deleting the Role it's associated with (or unregistering)
        # - "ID Shorthand" does not work
        # - REPORTED - Role Image is incorrectly represented
        # - REPORTED - Response body is empty in DELETE (#11)
        # - REPORTED - Filtering is very limited
        for action in reversed(cleanup_actions):
            action()
