/*
 *  Copyright (c) 2013 Croatia Control Ltd. (www.crocontrol.hr)
 *
 *  This file is part of Asterix.
 *
 *  Asterix is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Asterix is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with Asterix.  If not, see <http://www.gnu.org/licenses/>.
 *
 *
 * AUTHORS: Damir Salantic, Croatia Control Ltd.
 *
 */

#ifndef ASTERIXDATA_H_
#define ASTERIXDATA_H_

#include <map>

#include "AsterixDefinition.h"
#include "DataBlock.h"

class AsterixData
{
public:
  AsterixData();
  virtual
  ~AsterixData();

  std::list<DataBlock*> m_lDataBlocks;

#if defined(WIRESHARK_WRAPPER) || defined(ETHEREAL_WRAPPER)
  fulliautomatix_data* getData();
#endif

#if defined(PYTHON_WRAPPER)
  PyObject* getData();
#endif

  bool getText(std::string& strResult, const unsigned int formatType); // appends value to strResult in formatType format
};

#endif /* ASTERIXDATA_H_ */
