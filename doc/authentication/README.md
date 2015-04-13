Authentication
==============

Requests to the Scalr API are authenticated with a signature. The signature
is passed through 3 headers:

  + `X-Scalr-Key-Id`: YYYYYY
  + `X-Scalr-Signature`: XXXX
  + `X-Scalr-Date`: ISO 8601-formatted TZ-aware (or UTC) date and time.


Signature Algorithm
-------------------

### Signatures ###

The API signature format is: `<Signature Version> + <Space> + <Signature>`.

Currently:

  + `Signature Version` is the following string: `V1-HMAC-SHA256`
  + `Signature` is: base64-encoded HMAC of the canonical request signed using
    the API Secret Key  that corresponds to the API Key ID supplied in the
    `X-Scalr-Key-Id` Header.

### Canonical Request ###

The canonical request is defined as the following items joined by newlines (“\n”):

  + `Method`: uppercase HTTP method used (e.g. GET, POST)
  + `Date`: the ISO 8601-formatted date passed in the X-Scalr-Date header
  + `Path`: the path that was included in the request.
  + `Parameters`: canonical query string. See below for more information. If
    there are no parameters, this should be the empty string.
  + `Body`: The body of the request, as included in the request. If the request
    has no body (e.g. a GET request), this should be the empty string.


### Canonical Query String ###

Scalr uses the same format as AWS, with the added clarification that sorting
the pairs should be done prior to encoding them. Format follows:

  > Add the query string components (the name-value pairs, not including the initial question mark (?) as UTF-8 characters which are URL encoded per RFC 3986 (hexadecimal characters must be uppercased) and sorted using lexicographic byte ordering. Lexicographic byte ordering is case sensitive. 
  >
  > Separate parameter names from their values with the equal sign character (=) (ASCII character 61), even if the value is empty. Separate pairs of parameter and values with the ampersand character (&) (ASCII code 38). All reserved characters must be escaped. All unreserved characters must not be escaped. Concatenate the parameters and their values to make one long string with no spaces between them. Spaces within a parameter value, are allowed, but must be URL encoded as %20. In the concatenated string, period characters (.) are not escaped. RFC 3986 considers the period character an unreserved character, and thus it is not URL encoded. 
  >
  > *Note*
  >
  > RFC 3986 does not specify what happens with ASCII control characters, extended UTF-8 characters, and other characters reserved by RFC 1738. Since any values may be passed into a string value, these other characters should be percent encoded as %XY where X and Y are uppercase hex characters. Extended UTF-8 characters take the form %XY%ZA... (this handles multi-bytes). The space character should be represented as '%20'. Spaces should not be encoded as the plus sign (+) as this will cause as error.


Signature Validity
------------------

The signature is valid for 5 minutes before the date, and 5 minutes after the
date passed in `X-Scalr-Date`.


`X-Scalr-Debug`
---------------

We currently support an additional header (`X-Scalr-Debug`) that,
when set to 1, causes Scalr to return the canonical request, to help users
debug their implementation (this has no security impact either, considering
that if an attacker sees the request, they could compute the canonical request
anyway, but that doesn't help them sign it).
