'''
Copyright 2017, United States Government, as represented by the Administrator of the National Aeronautics and Space
Administration. All rights reserved.

The pyCMR platform is licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

'''
import errno
import shutil
import urllib
from os import makedirs
from os.path import dirname, exists, isdir
import logging

import requests

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

if not hasattr(urllib, 'urlretrieve'):
    urlretrieve = urllib.request.urlretrieve  # 3.0 and later
else:
    urlretrieve = urllib.urlretrieve


def mkdir_p(path):
    try:
        makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and isdir(path):
            pass
        else:
            raise


class Result(dict):
    """
    The class to structure the response xml string from the cmr API
    """
    _location = None

    def __init__(self, metaResult):
        for k in metaResult:
            self[k] = metaResult[k]

    def download(self, destpath=".", unm=None, pwd=None):
        """
        Download the dataset into file system
        :param destpath: path for downloaded files. Use current directory by default.
        :param unm: username if needed for ftp download
        :param pwd: password if needed for ftp download
        :return:
        """
        url = self.getDownloadUrl()
        # Downloadable url does not exist
        if not url:
            raise ValueError("no download url found")
        # make dirs recursively on user destination path as on the remote side
        destpath = destpath + "/" + url[url.find('allData'):]
        mkdir_p(dirname(destpath))
        # if no file exists
        if not exists(destpath):

            if url.startswith('ftp'):
                # if data is downloaded from the NRT server, need uname/pwd
                if 'nrt' in url:
                    url = url.replace('ftp://', 'ftp://' + unm + ':' + pwd + '@')
                urlretrieve(url, destpath)
            else:
                r = requests.get(url, stream=True)
                r.raw.decode_content = True

                with open(destpath + "/" + self._downloadname.replace('/', ''), 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
        else:
            print('File {} already exists'.format(destpath))

    def getDownloadUrl(self):
        """
        :return:
        """
        if self._location is not None:
            return self._location
        else:
            # TODO: do json request & parse results


class Collection(Result):
    def __init__(self, metaResult, cmr_host):
        super(Collection, self).__init__(metaResult)

        self._location = 'https://{}/search/concepts/{}.umm-json'.format(cmr_host, metaResult['concept-id'])
        self._downloadname = metaResult['Collection']['ShortName']


class Granule(Result):
    def __init__(self, metaResult):
        super(Granule, self).__init__(metaResult)

    def getOPeNDAPUrl(self):
        return self._OPeNDAPUrl
