
#ifndef SHAREDMEM_H
#define SHAREDMEM_H

#include <boost/interprocess/mapped_region.hpp>
#include <boost/interprocess/shared_memory_object.hpp>
#include <string>
#include <stdio.h>

using namespace boost::interprocess;

class SharedMemory {
public:
	mapped_region region;
    unsigned char shared[128];
    permissions perms;
    shared_memory_object shdmem;
    std::string mem_name;

    void open();

    void setValue(unsigned int, unsigned int);

    void update();

    void copy(unsigned char* from);

    void close();
};

#endif // SHAREDMEM_H
