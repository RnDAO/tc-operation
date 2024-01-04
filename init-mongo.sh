#!/usr/bin/env bash
set -eu
mongosh -- "$MONGO_INITDB_DATABASE" <<EOF
    var rootUser = '$MONGO_INITDB_ROOT_USERNAME';
    var rootPassword = '$MONGO_INITDB_ROOT_PASSWORD';
    var admin = db.getSiblingDB('admin');
    admin.auth(rootUser, rootPassword);

    var rootUser = '$MONGO_INITDB_ROOT_USERNAME';
    var rootPassword = '$MONGO_INITDB_ROOT_PASSWORD';
    db.createUser({user: rootUser, pwd: rootPassword, roles: ["readWrite"]});

    # REPLICA SET
    # var config = {
    #     "_id": "dbrs",
    #     "version": 1,
    #     "members": [
    #         {
    #             "_id": 1,
    #             "host": "mongodb-dev:27017",
    #             "priority": 1
    #         },
    #     ]
    # };

    # rs.initiate(config, { force: true })
    # rs.status()
EOF
