


#include <boost/interprocess/creation_tags.hpp>
#include <boost/interprocess/detail/os_file_functions.hpp>
#include <boost/interprocess/mapped_region.hpp>
#include <boost/interprocess/permissions.hpp>
#include <boost/interprocess/shared_memory_object.hpp>
#include <sys/stat.h>
#include <syslog.h>
#include <algorithm>
#include <cstring>
#include <functional>
#include <iterator>
#include <string>
#include <stdio.h>
#include "sharedmem.h"

using namespace boost::interprocess;

struct shm_remove
{
   shm_remove() { shared_memory_object::remove("sixaxis_controller_1"); }
   ~shm_remove(){ shared_memory_object::remove("sixaxis_controller_1"); }
} remover;


void SharedMemory::open() {
	mem_name = "sixaxis_controller_1";
	permissions perms(0644); // 0644
	unsigned int old_mask = umask(0);
	shdmem = shared_memory_object (
		open_or_create, mem_name.c_str(),
		read_write, perms);
	umask(old_mask);
	shdmem.truncate(128 * sizeof(unsigned char));
	region = mapped_region(shdmem, read_write);
	shared[0] = 1; // test bytes
	shared[1] = 2;
	shared[2] = 3;
	shared[3] = 4;
	syslog(LOG_INFO, "Length of a value:%lu", sizeof(unsigned char));
	std::memset(region.get_address(), 1, region.get_size());
	std::memcpy(region.get_address(), shared, sizeof(shared));
	syslog(LOG_INFO, "Shared Memory Name:%s", shdmem.get_name());
	std::string s; s.reserve(128 * sizeof(*shared));
	std::transform(shared, shared + 128, std::back_inserter(s),
				   std::bind1st(std::plus<int>(), '0'));
//				syslog(LOG_INFO, "Values:%s", out);
	syslog(LOG_INFO, "Values:%s", s.c_str());
}

void SharedMemory::setValue(unsigned int b, unsigned int index) {
	shared[index] = b;
}

void SharedMemory::update() {
	std::memcpy(region.get_address(), shared, sizeof(shared));
}

void SharedMemory::copy(unsigned char* from) {
	std::memcpy(region.get_address(), from, 128 * sizeof(from));
}

void SharedMemory::close() {
	shared_memory_object::remove("sixaxis_controller_1");
}


