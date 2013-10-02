#!/usr/bin/env python2.7
#
# Copyright (C) 2013 DNAnexus, Inc.
#
# This file is part of dx-toolkit (DNAnexus platform client libraries).
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may not
#   use this file except in compliance with the License. You may obtain a copy
#   of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import sys, json

preamble = '''/* Do not modify this file by hand.
 *
 * It is automatically generated by src/api_wrappers/generateJavaAPIWrappers.py.
 * (Run make api_wrappers to update it.)
 */

package com.dnanexus;

import com.dnanexus.DXHTTPRequest;
import com.dnanexus.DXEnvironment;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Low-level wrappers for invoking DNAnexus API methods.
 */
public class DXAPI {

    private static ObjectMapper mapper = new ObjectMapper();
'''

postscript = '''}
'''

class_method_template = '''
    /**
     * Invokes the {method_name} method.{wiki_link}
     */
    public static JsonNode {method_name}() throws Exception {{
        return {method_name}(mapper.readTree("{{}}"));
    }}
    /**
     * Invokes the {method_name} method with the specified input parameters.{wiki_link}
     *
     * @param inputParams input parameters to the API call
     */
    public static JsonNode {method_name}(JsonNode inputParams) throws Exception {{
        return new DXHTTPRequest().request("{route}", inputParams);
    }}
    /**
     * Invokes the {method_name} method with the specified environment and input parameters.{wiki_link}
     *
     * @param inputParams input parameters to the API call
     */
    public static JsonNode {method_name}(JsonNode inputParams, DXEnvironment env) throws Exception {{
        return new DXHTTPRequest(env).request("{route}", inputParams);
    }}'''

object_method_template = '''
    /**
     * Invokes the {method_name} method.{wiki_link}
     *
     * @param objectId ID of the object to operate on
     */
    public static JsonNode {method_name}(String objectId) throws Exception {{
        return {method_name}(objectId, mapper.readTree("{{}}"));
    }}
    /**
     * Invokes the {method_name} method with the specified parameters.{wiki_link}
     *
     * @param objectId ID of the object to operate on
     * @param inputParams input parameters to the API call
     */
    public static JsonNode {method_name}(String objectId, JsonNode inputParams) throws Exception {{
        return new DXHTTPRequest().request("/" + objectId + "/" + "{method_route}", inputParams);
    }}
    /**
     * Invokes the {method_name} method with the specified environment and parameters.{wiki_link}
     *
     * @param objectId ID of the object to operate on
     * @param inputParams input parameters to the API call
     */
    public static JsonNode {method_name}(String objectId, JsonNode inputParams, DXEnvironment env) throws Exception {{
        return new DXHTTPRequest(env).request("/" + objectId + "/" + "{method_route}", inputParams);
    }}'''

#app_object_method_template = '''
#def {method_name}(app_name_or_id, alias=None, input_params={{}}, **kwargs):
#    fully_qualified_version = app_name_or_id + (('/' + alias) if alias else '')
#    return DXHTTPRequest('/%s/{method_route}' % fully_qualified_version, input_params, **kwargs)
#'''
app_object_method_template = object_method_template

print preamble

for method in json.loads(sys.stdin.read()):
    route, signature, opts = method
    method_name = signature.split("(")[0]
    wiki_link = ''
    if opts.get('wikiLink', None):
        wiki_link = '\n     *\n     * <p>For more information about this method, see the <a href="%s">API specification</a>.' % (opts['wikiLink'],)
    if (opts['objectMethod']):
        root, oid_route, method_route = route.split("/")
        if oid_route == 'app-xxxx':
            print app_object_method_template.format(method_name=method_name, method_route=method_route, wiki_link=wiki_link)
        else:
            print object_method_template.format(method_name=method_name, method_route=method_route, wiki_link=wiki_link)
    else:
        print class_method_template.format(method_name=method_name, route=route, wiki_link=wiki_link)

print postscript
