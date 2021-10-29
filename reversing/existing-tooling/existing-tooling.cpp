#include <iostream>
#include <cstring>
#include "obfuscate.h"

int main(int argc, char **argv) {
  std::cout << "The flag is " 
            << strlen(AY_OBFUSCATE("gigem{im_curious_did_you_statically_or_dynamically_reverse_ping_addison}"))
            << " characters long."
            << std::endl;
}
