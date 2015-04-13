Scalr APIv2 Provisional Documentation
=====================================

This repository contains provisional documentation for the upcoming Scalr
APIv2.

**Note that this documentation as well as the API it describes are subject to
change.**


Using this Documentation
------------------------

### Endpoints ###

The endpoints currently exposed in the API are available under the
[`doc/rest/api/user/v1`](./doc/rest/api/user/v1) path. Directories map to endpoints,
and files map to methods.

For example, [`doc/rest/api/user/v1/{envId}/events/GET.mkd`](./doc/rest/api/user/v1/{envId}/events/GET.mkd)
is documentation for the `GET` method on the `/api/user/v1/{envId}/events/`
endpoint.

### Definitions ###

The [`definitions`](./doc/definitions) folder includes documentation for the
objects that are manipulated using the Scalr API.


### Authentication ###

If you'd like to write your own API Client, review the documentation under
[`doc/authentication`](./doc/authentication).


Getting Started
---------------

### Enable APIv2 ###

To get started with APIv2, you should first enable APIv2 in your Scalr install.
To do so, include the following in your `/etc/scalr-server/scalr-server.rb`
file:

    app[:configuration] = {
      :scalr => {
        :system => {
          :api => {
            :enabled => true
          },
        },
      },
    }

Note that if you already have a `app[:configuration]`, you should instead
merge this in.


### Generate an API Key ###

Login as the user you'd like to access the API as, and access the following
URL:

    http://your-scalr-host/#/core/api2

Then, generate a new key.


### Code Samples ###

Get started with the code samples here: [`samples`](./samples).
