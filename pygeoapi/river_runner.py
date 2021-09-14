# =================================================================
#
# Authors: Benjamin Webb <benjamin.miller.webb@gmail.com>
#
# Copyright (c) 2021 Benjamin Webb
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import os
import logging

from pygeoapi.util import yaml_load
from pygeoapi.plugin import load_plugin
from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError


LOGGER = logging.getLogger(__name__)
CONFIG_ = ''

with open(os.getenv('PYGEOAPI_CONFIG'), encoding='utf8') as fh:
    CONFIG_ = yaml_load(fh)

PROVIDER_DEF = CONFIG_['resources']['merit']['providers'][0]
P = 'properties'
#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.1.0',
    'id': 'river-runner',
    'title': {
        'en': 'River Runner'
    },
    'description': {
        'en': 'A simple process that takes a lat/lng or bbox as input, '
              'and returns the largest flowpath.'
    },
    'keywords': ['river runner', 'rivers'],
    'links': [{
        'type': 'text/html',
        'rel': 'canonical',
        'title': 'information',
        'href': 'https://example.org/process',
        'hreflang': 'en-US'
    }],
    'inputs': {
        'bbox': {
            'title': 'Boundary Box',
            'description': 'A set of four coordinates',
            'schema': {
                'type': 'object',
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['coordinates', 'geography']
        },
        'latlng': {
            'title': 'Latitude & Longitude',
            'description': 'A set of two coordinates',
            'schema': {
                'type': 'object',
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['coordinates', 'latitude', 'longitude']
        },
        'lat': {
            'title': 'Latitude',
            'description': 'Latitude of a point',
            'schema': {
                'type': 'number',
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['coordinates', 'latitude']
        },
        'lng': {
            'title': 'Longitude',
            'description': 'Longitude of a point',
            'schema': {
                'type': 'number',
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['coordinates', 'longitude']
        }
    },
    'outputs': {
        'echo': {
            'title': 'Feature Collection',
            'description': 'A geoJSON Feature Collection of River Runner',
            'schema': {
                'type': 'Object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'bbox': [-86.2, 39.7, -86.15, 39.75]
        }
    }
}


class RiverRunnerProcessor(BaseProcessor):
    """River Runner Processor example"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.process.river_runner.RiverRunnerProcessor
        """
        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data):
        mimetype = 'application/json'
        outputs = {
                'id': 'echo',
                'value': {
                    'type': 'FeatureCollection',
                    'features': []
                }
            }

        if not data.get('bbox') and not data.get('latlng') and \
           (not data.get('lat') and not data.get('lng')):
            raise ProcessorExecuteError(f'Invalid input: { {{data.items()}} }')

        for k, v in data.items():
            if isinstance(v, str):
                data[k] = ','.join(v.split(',')).strip('()[]')
                if k in ['latlng', 'bbox']:
                    data[k] = data[k].split(',')

        if data.get('bbox', []):
            bbox = data.get('bbox')
        elif data.get('latlng', ''):
            bbox = data.get('latlng')
        else:
            bbox = (data.get('lng'), data.get('lat'))

        bbox = bbox * 2 if len(bbox) == 2 else bbox
        bbox = self._expand_bbox(bbox)

        p = load_plugin('provider', PROVIDER_DEF)   
        value = p.query(bbox=bbox)
        i = 1
        while len(value['features']) < 1 and i < 3:
            LOGGER.debug(f'No features in bbox {bbox}, expanding')
            bbox = self._expand_bbox(bbox, e=0.5*i)
            value = p.query(bbox=bbox)
            i = i + 1

        if len(value['features']) < 1:
            LOGGER.debug('No features found')
            return mimetype, outputs

        LOGGER.debug('fetching downstream features')
        mh = self._compare(value, 'hydroseq', min)
        out, trim = [], []
        for i in (mh[P]['levelpathi'],
                  *mh[P]['down_levelpaths'].split(',')):
            try:
                i = int(float(i))
            except ValueError:
                LOGGER.error(f'No Downstem Rivers found {i}')
                continue

            down = p.query(
                properties=[('levelpathi', i), ], limit=1000
                )

            out.extend(down['features'])
            m = self._compare(down, 'hydroseq', min)
            trim.append((m[P]['dnlevelpat'], m[P]['dnhydroseq']))

        LOGGER.debug('keeping only mainstem flowpath')
        trim.append((mh[P]['levelpathi'], mh[P]['hydroseq']))
        outm = []
        for seg in out:
            for i in trim:
                if seg[P]['levelpathi'] == i[0] and \
                   seg[P]['hydroseq'] <= i[1]:
                    outm.append(seg)

        value['features'] = outm
        outputs = {
            'id': 'echo',
            'value': value
        }
        return mimetype, outputs

    def _compare(self, fc, prop, dir):
        val = fc['features'][0]
        for f in fc['features']:
            if dir(f[P][prop], val[P][prop]) != val[P][prop]:
                val = f
        return val

    def _expand_bbox(self, bbox, e=0.125):
        return [float(b) + e if i < 2 else float(b) - e
                for (i, b) in enumerate(bbox)]

    def __repr__(self):
        return '<RiverRunnerProcessor> {}'.format(self.name)
