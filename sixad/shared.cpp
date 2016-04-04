/*
 * shared.cpp
 *
 * This file is part of the QtSixA, the Sixaxis Joystick Manager
 * Copyright 2008-2011 Filipe Coelho <falktx@gmail.com>
 *
 * QtSixA can be redistributed and/or modified under the terms of the GNU General
 * Public License (Version 2), as published by the Free Software Foundation.
 * A copy of the license is included in the QtSixA source code, or can be found
 * online at www.gnu.org/licenses.
 *
 * QtSixA is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
 * A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 */

#include "shared.h"
#include "textfile.h"

#include <cstdio>
#include <cstring>
#include <fcntl.h>
#include <signal.h>
#include <syslog.h>
#include <unistd.h>
#include <sys/socket.h>
#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <semaphore.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <stdarg.h>

#include "configuration.cpp"

static volatile sig_atomic_t __active = false;
static volatile sig_atomic_t __io_canceled = false;

bool was_active()
{
  return __active;
}

void set_active(int active)
{
  __active = active;
}

bool io_canceled()
{
  return __io_canceled;
}

void sig_term(int /* sig */)
{
    __io_canceled = 1;
}

void open_log(const char *app_name)
{
    openlog(app_name, LOG_NDELAY|LOG_PID|LOG_PERROR, LOG_DAEMON);
}

struct device_settings init_values(const char *addr)
{
    struct device_settings settings;

    char pathname[64];
    strcpy(pathname, "/var/lib/sixad/profiles/");
    strcat(pathname, addr);

    if (open(pathname, O_RDONLY) > 0) {

        settings.led.enabled = textfile_get_int(pathname, "enable_leds", 1);
        settings.led.auto_sel = textfile_get_int(pathname, "led_n_auto", 1);
        settings.led.number = textfile_get_int(pathname, "led_n_number", 1);
        settings.led.anim = textfile_get_int(pathname, "led_anim", 1);

        settings.joystick.enabled = textfile_get_int(pathname, "enable_joystick", 1);
        settings.joystick.buttons = textfile_get_int(pathname, "enable_buttons", 1);
        settings.joystick.sbuttons = textfile_get_int(pathname, "enable_sbuttons", 1);
        settings.joystick.axis  = textfile_get_int(pathname, "enable_axis", 1);
        settings.joystick.accel = textfile_get_int(pathname, "enable_accel", 1);
        settings.joystick.accon = textfile_get_int(pathname, "enable_accon", 0);
        settings.joystick.speed = textfile_get_int(pathname, "enable_speed", 0);
        settings.joystick.pos = textfile_get_int(pathname, "enable_pos", 0);

        settings.remote.enabled = textfile_get_int(pathname, "enable_remote", 1);
        settings.remote.numeric = textfile_get_int(pathname, "remote_numberic", 1);
        settings.remote.dvd = textfile_get_int(pathname, "remote_dvd", 1);
        settings.remote.directional = textfile_get_int(pathname, "remote_directional", 1);
        settings.remote.multimedia = textfile_get_int(pathname, "remote_multimedia", 1);

        settings.input.enabled = textfile_get_int(pathname, "enable_input", 0);
        settings.input.key_select = textfile_get_int(pathname, "key_select", 0);
        settings.input.key_l3 = textfile_get_int(pathname, "key_l3", 0);
        settings.input.key_r3 = textfile_get_int(pathname, "key_r3", 0);
        settings.input.key_start = textfile_get_int(pathname, "key_start", 0);
        settings.input.key_up    = textfile_get_int(pathname, "key_up", 0);
        settings.input.key_right = textfile_get_int(pathname, "key_right", 0);
        settings.input.key_down  = textfile_get_int(pathname, "key_down", 0);
        settings.input.key_left  = textfile_get_int(pathname, "key_left", 0);
        settings.input.key_l2  = textfile_get_int(pathname, "key_l2", 0);
        settings.input.key_r2  = textfile_get_int(pathname, "key_r2", 0);
        settings.input.key_l1  = textfile_get_int(pathname, "key_l1", 0);
        settings.input.key_r1  = textfile_get_int(pathname, "key_r1", 0);
        settings.input.key_tri = textfile_get_int(pathname, "key_tri", 0);
        settings.input.key_cir = textfile_get_int(pathname, "key_cir", 0);
        settings.input.key_squ = textfile_get_int(pathname, "key_squ", 0);
        settings.input.key_cro = textfile_get_int(pathname, "key_cro", 0);
        settings.input.key_ps  = textfile_get_int(pathname, "key_ps", 0);
        settings.input.axis_l_type  = textfile_get_int(pathname, "axis_left_type", 0);
        settings.input.axis_l_up    = textfile_get_int(pathname, "axis_left_up", 0);
        settings.input.axis_l_right = textfile_get_int(pathname, "axis_left_right", 0);
        settings.input.axis_l_down  = textfile_get_int(pathname, "axis_left_down", 0);
        settings.input.axis_l_left  = textfile_get_int(pathname, "axis_left_left", 0);
        settings.input.axis_r_type  = textfile_get_int(pathname, "axis_right_type", 0);
        settings.input.axis_r_up    = textfile_get_int(pathname, "axis_right_up", 0);
        settings.input.axis_r_right = textfile_get_int(pathname, "axis_right_right", 0);
        settings.input.axis_r_down  = textfile_get_int(pathname, "axis_right_down", 0);
        settings.input.axis_r_left  = textfile_get_int(pathname, "axis_right_left", 0);
        settings.input.axis_speed = (10 - textfile_get_int(pathname, "axis_speed", 6));
        settings.input.use_lr3 = textfile_get_int(pathname, "use_lr3", 0);

        settings.rumble.enabled = textfile_get_int(pathname, "enable_rumble", 1);
        settings.rumble.old_mode = textfile_get_int(pathname, "old_rumble_mode", 0);

        settings.timeout.enabled = textfile_get_int(pathname, "enable_timeout", 1);
        settings.timeout.timeout = textfile_get_int(pathname, "timeout_mins", 30);

        settings.auto_disconnect = (bool)textfile_get_int(pathname, "out_of_reach_disconnects", 0);

    } else if (open("/var/lib/sixad/profiles/default", O_RDONLY) > 0) { //default config
        strcpy(pathname, "/var/lib/sixad/profiles/default");

        settings.led.enabled = textfile_get_int(pathname, "enable_leds", 1);
        settings.led.auto_sel = textfile_get_int(pathname, "led_n_auto", 1);
        settings.led.number = textfile_get_int(pathname, "led_n_number", 1);
        settings.led.anim = textfile_get_int(pathname, "led_anim", 1);

        settings.joystick.enabled = textfile_get_int(pathname, "enable_joystick", 1);
        settings.joystick.buttons = textfile_get_int(pathname, "enable_buttons", 1);
        settings.joystick.sbuttons = textfile_get_int(pathname, "enable_sbuttons", 1);
        settings.joystick.axis  = textfile_get_int(pathname, "enable_axis", 1);
        settings.joystick.accel = textfile_get_int(pathname, "enable_accel", 1);
        settings.joystick.accon = textfile_get_int(pathname, "enable_accon", 0);
        settings.joystick.speed = textfile_get_int(pathname, "enable_speed", 0);
        settings.joystick.pos = textfile_get_int(pathname, "enable_pos", 0);

        settings.remote.enabled = textfile_get_int(pathname, "enable_remote", 1);
        settings.remote.numeric = textfile_get_int(pathname, "remote_numberic", 1);
        settings.remote.dvd = textfile_get_int(pathname, "remote_dvd", 1);
        settings.remote.directional = textfile_get_int(pathname, "remote_directional", 1);
        settings.remote.multimedia = textfile_get_int(pathname, "remote_multimedia", 1);

        settings.input.enabled = textfile_get_int(pathname, "enable_input", 0);
        settings.input.key_select = textfile_get_int(pathname, "key_select", 0);
        settings.input.key_l3 = textfile_get_int(pathname, "key_l3", 0);
        settings.input.key_r3 = textfile_get_int(pathname, "key_r3", 0);
        settings.input.key_start = textfile_get_int(pathname, "key_start", 0);
        settings.input.key_up    = textfile_get_int(pathname, "key_up", 0);
        settings.input.key_right = textfile_get_int(pathname, "key_right", 0);
        settings.input.key_down  = textfile_get_int(pathname, "key_down", 0);
        settings.input.key_left  = textfile_get_int(pathname, "key_left", 0);
        settings.input.key_l2  = textfile_get_int(pathname, "key_l2", 0);
        settings.input.key_r2  = textfile_get_int(pathname, "key_r2", 0);
        settings.input.key_l1  = textfile_get_int(pathname, "key_l1", 0);
        settings.input.key_r1  = textfile_get_int(pathname, "key_r1", 0);
        settings.input.key_tri = textfile_get_int(pathname, "key_tri", 0);
        settings.input.key_cir = textfile_get_int(pathname, "key_cir", 0);
        settings.input.key_squ = textfile_get_int(pathname, "key_squ", 0);
        settings.input.key_cro = textfile_get_int(pathname, "key_cro", 0);
        settings.input.key_ps  = textfile_get_int(pathname, "key_ps", 0);
        settings.input.axis_l_type  = textfile_get_int(pathname, "axis_left_type", 0);
        settings.input.axis_l_up    = textfile_get_int(pathname, "axis_left_up", 0);
        settings.input.axis_l_right = textfile_get_int(pathname, "axis_left_right", 0);
        settings.input.axis_l_down  = textfile_get_int(pathname, "axis_left_down", 0);
        settings.input.axis_l_left  = textfile_get_int(pathname, "axis_left_left", 0);
        settings.input.axis_r_type  = textfile_get_int(pathname, "axis_right_type", 0);
        settings.input.axis_r_up    = textfile_get_int(pathname, "axis_right_up", 0);
        settings.input.axis_r_right = textfile_get_int(pathname, "axis_right_right", 0);
        settings.input.axis_r_down  = textfile_get_int(pathname, "axis_right_down", 0);
        settings.input.axis_r_left  = textfile_get_int(pathname, "axis_right_left", 0);
        settings.input.axis_speed = (10 - textfile_get_int(pathname, "axis_speed", 6));
        settings.input.use_lr3 = textfile_get_int(pathname, "use_lr3", 0);

        settings.rumble.enabled = textfile_get_int(pathname, "enable_rumble", 1);
        settings.rumble.old_mode = textfile_get_int(pathname, "old_rumble_mode", 0);

        settings.timeout.enabled = textfile_get_int(pathname, "enable_timeout", 1);
        settings.timeout.timeout = textfile_get_int(pathname, "timeout_mins", 30);

        settings.auto_disconnect = (bool)textfile_get_int(pathname, "out_of_reach_disconnects", 0);

    } else { // no config

        settings.led.enabled = 1;
        settings.led.auto_sel = 1;
        settings.led.number = 1;
        settings.led.anim = 1;

        settings.joystick.enabled = 1;
        settings.joystick.buttons = 1;
        settings.joystick.sbuttons = 1;
        settings.joystick.axis  = 1;
        settings.joystick.accel = 1;
        settings.joystick.accon = 0;
        settings.joystick.speed = 0;
        settings.joystick.pos = 0;

        settings.remote.enabled = 1;
        settings.remote.numeric = 1;
        settings.remote.dvd = 1;
        settings.remote.directional = 1;
        settings.remote.multimedia = 1;

        settings.input.enabled = 0;
        settings.input.key_select = 0;
        settings.input.key_l3 = 0;
        settings.input.key_r3 = 0;
        settings.input.key_start = 0;
        settings.input.key_up    = 0;
        settings.input.key_right = 0;
        settings.input.key_down  = 0;
        settings.input.key_left  = 0;
        settings.input.key_l2  = 0;
        settings.input.key_r2  = 0;
        settings.input.key_l1  = 0;
        settings.input.key_r1  = 0;
        settings.input.key_tri = 0;
        settings.input.key_cir = 0;
        settings.input.key_squ = 0;
        settings.input.key_cro = 0;
        settings.input.key_ps  = 0;
        settings.input.axis_l_type = 0;
        settings.input.axis_l_up = 0;
        settings.input.axis_l_right = 0;
        settings.input.axis_l_down = 0;
        settings.input.axis_l_left = 0;
        settings.input.axis_r_type = 0;
        settings.input.axis_r_up = 0;
        settings.input.axis_r_right = 0;
        settings.input.axis_r_down = 0;
        settings.input.axis_r_left = 0;
        settings.input.axis_speed = 6;
        settings.input.use_lr3 = 0;

        settings.rumble.enabled = 1;
        settings.rumble.old_mode = 0;

        settings.timeout.enabled = 1;
        settings.timeout.timeout = 30;

        settings.auto_disconnect = false;
    }

    return settings;
}

int get_joystick_number()
{
    int i, js;
    char jspath[16];

    js = 1;
    for (i=0; i < 10; i++) {
        snprintf(jspath, sizeof(jspath), "/dev/input/js%i", i);
        if (open(jspath, O_RDONLY) > 0) {
            js = i+1;
        }
    }

    return js;
}

void enable_sixaxis(int csk)
{
    char buf[128];

    unsigned char enable[] = {
        0x53, /* HIDP_TRANS_SET_REPORT | HIDP_DATA_RTYPE_FEATURE */
        0xf4, 0x42, 0x03, 0x00, 0x00
    };

    /* enable reporting */
    send(csk, enable, sizeof(enable), 0);
    recv(csk, buf, sizeof(buf), 0);
}


class SharedMemory {
private:
    int fd;
    int rc;
    sem_t *pSemaphore = NULL;
    void *pSharedMemory = NULL;
    char last_message[256];
public:
	void static init(Config config) {
        // setup shared memory for QtSixA
        int fd = shm_open(config.shared_mem_name, O_RDWR | O_CREAT | O_EXCL, Config::ipc_permissions);
        if (fd == -1) {
			fd = 0;
			syslog(LOG_ERR, "Creating shared memory faild!");
		}
        else {
            // Set shared memory size
            rc = ftruncate(fd, Config::shm_size);
            if (rc) {
    			syslog(LOG_ERR, "Resizing the shared memory failed!");
            }
            else {
                // MMap the shared memory
                //void *mmap(void *start, size_t length, int prot, int flags, int fd, off_t offset);
                pSharedMemory = mmap((void *)0, (size_t)Config::shm_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
                if (pSharedMemory == MAP_FAILED) {
                    pSharedMemory = NULL;
        			syslog(LOG_ERR, "MMapping the shared memory failed!");
                }
                else {
        			syslog(LOG_ERR, "pSharedMemory = %p", pSharedMemory);
                }
            }
        }


        if (pSharedMemory) {
            // Create the semaphore
            pSemaphore = sem_open(Config::semaphore_name, O_CREAT, Config::ipc_permissions, 0);

            if (pSemaphore == SEM_FAILED) {
    			syslog(LOG_ERR, "Creating the semaphore failed!");
            }
            else {
    			syslog(LOG_ERR, "The semaphore is %p", (void *)pSemaphore);

                // I seed the shared memory with a random string (the current time).
                get_current_time(s);

                strcpy((char *)pSharedMemory, "test");
                strcpy(last_message, "test");

                syslog(LOG_INFO, "Wrote %zu characters: %s", strlen(last_message), last_message);

            }
        }

	}

	void static strcopy(const char* str) {
        rc = acquire_semaphore(pSemaphore, Config::semaphore);
        strcpy((char *)pSharedMemory, str);
        rc = release_semaphore(pSemaphore, Config::semaphore);
	}

	void static closesm() {
        rc = acquire_semaphore(pSemaphore, Config::semaphore);
        if (!rc) {
			syslog(LOG_NOTICE, "Destroying shared memory...");

            // Un-mmap the memory...
            rc = munmap(pSharedMemory, (size_t)Config::shm_size);
            if (rc) {
    			syslog(LOG_ERR, "Unmapping the memory failed!");
            }

            // ...close the file descriptor...
            if (-1 == close(fd)) {
    			syslog(LOG_ERR, "Closing the memory's file descriptor failed!");
            }

            // ...and destroy the shared memory.
            rc = shm_unlink(Config::shared_mem_name);
            if (rc) {
    			syslog(LOG_ERR, "Unlinking the memory failed!");
            }
        }
        // Clean up the semaphore
        rc = sem_close(pSemaphore);
        if (rc) {
			syslog(LOG_NOTICE, "Shared memory closed.");
        }
        rc = sem_unlink(Config::semaphore_name);
        if (rc) {
			syslog(LOG_NOTICE, "Unlinking the semaphore failed!");
        }
    }
};

int release_semaphore(sem_t *pSemaphore, int live_dangerously) {
    int rc = 0;
    char s[1024];

    if (!live_dangerously) {
        rc = sem_post(pSemaphore);
        if (rc) {
			syslog(LOG_ERR, "Releasing the semaphore failed!");
        }
    }

    return rc;
}


int acquire_semaphore(sem_t *pSemaphore, int live_dangerously) {
    int rc = 0;
    char s[1024];

    if (!live_dangerously) {
        rc = sem_wait(pSemaphore);
        if (rc) {
			syslog(LOG_ERR, "Acquiring the semaphore failed!");
        }
    }

    return rc;
}


void get_current_time(char *s) {
    time_t the_time;
    struct tm *the_localtime;
    char *pAscTime;

    the_time = time(NULL);
    the_localtime = localtime(&the_time);
    pAscTime = asctime(the_localtime);

    strcpy(s, pAscTime);
}

