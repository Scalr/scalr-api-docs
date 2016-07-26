(function() {

  ScalrAPI = {};

  ScalrAPI.signatureVersion = 'V1-HMAC-SHA256';

  ScalrAPI.apiSettings = {};

  ScalrAPI.setSettings = function(newSettings) {
    this.apiSettings = newSettings;
  }

  ScalrAPI.makeQueryString = function(params) {
    if (params.length == 0) {
      return '';
    }
    if (JSON.stringify(params) === '{}') {
      return '';
    }
    var sorted = [];
    for(var key in params) {
      sorted[sorted.length] = key;
    }
    sorted.sort();
    var result = encodeURIComponent(sorted[0]) + '=' + encodeURIComponent(params[sorted[0]]);
    for (var i = 1; i < sorted.length; i ++) {
      result += '&' + encodeURIComponent(sorted[i]) + '=' + encodeURIComponent(params[sorted[1]]);
    }
    return result;
  }

  ScalrAPI.makeAuthHeaders = function(method, date, path, params, body) {
    var headers = {'X-Scalr-Key-Id': this.apiSettings.keyId,
                   'X-Scalr-Date' : date,
                   'X-Scalr-Debug' : '1'};
    var toSign = [method, date, path, params, body].join('\n');

    var signature = CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(toSign, this.apiSettings.secretKey));

    headers['X-Scalr-Signature'] = this.signatureVersion + ' ' + signature;
    return headers;
  }

  ScalrAPI.makeApiCall = function (method, path, params, body, onSuccess, onError) {
    var queryString, headers;
    var timestamp = new Date().toISOString();
    var scalrAddress = this.apiSettings.apiUrl;

    if (!params) {
      queryString = '';
    } else if (typeof params === 'string') {
      queryString = params; //Assuming the parameters are sorted if they are passed as a string
    } else {
      queryString = this.makeQueryString(params);
    }

    if (scalrAddress.endsWith('/')) {
      scalrAddress = scalrAddress.substring(0, scalrAddress.length - 1);
    }

    headers = this.makeAuthHeaders(method, timestamp, path, queryString, body);

    $.ajax({
      type: method,
      url: scalrAddress + path + (queryString.length > 0 ? '?' + queryString : ''),
      data: body,
      headers: headers,
      success: onSuccess,
      error: onError
    });
  }

  ScalrAPI.fetch = function(path, params, onSuccess, onError) {
    this.makeApiCall('GET', path, params, '', onSuccess, onError);
  }

  ScalrAPI.create = function(path, body, params, onSuccess, onError) {
    this.makeApiCall('POST', path, params, body, onSuccess, onError);
  }

  ScalrAPI.delete = function(path, params, onSuccess, onError) {
    this.makeApiCall('DELETE', path, params, '', onSuccess, onError);
  }

  ScalrAPI.edit = function(path, body, params, onSuccess, onError) {
    this.makeApiCall('PATCH', path, params, body, onSuccess, onError);
  }

  // Note: with this function the response object passed to the onSuccess will be the one returned by the last API call
  // of the scroll, to which a new property all_data is added, containing the parsed representation of all the results.
  ScalrAPI.scroll = function(path, params, onSuccess, onError) {
    this.makeApiCall('GET', path, params, '', 
      this.makeOnScrollSuccess(path, onSuccess, onError, [], this),
      onError);
  }

  ScalrAPI.makeOnScrollSuccess = function(path, onSuccess, onError, previousData, that) {
    return function(response) {
      var result = response.data;
      var data = result.data.concat(previousData);

      if (result.pagination.next) {
        var nextParams = result.pagination.next.substring(result.pagination.next.indexOf('?') + 1);
        that.makeApiCall('GET', path, nextParams, '', 
          that.makeOnScrollSuccess(path, onSuccess, onError, data, that),
          onError);
      } else {
        response.all_data = data;
        onSuccess(response);
      }
    };
  }

  var root = this;

  // CommonJS/nodeJS Loader
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = showdown;

  // AMD Loader
  } else if (typeof define === 'function' && define.amd) {
    define(function () {
      'use strict';
      return ScalrAPI;
    });

  // Regular Browser loader
  } else {
    root.ScalrAPI = ScalrAPI;
  }

}.call(this));
