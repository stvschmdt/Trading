#ifndef SHARE_H_
#define SHARE_H_

#include "headers.h"

class Share{
    public:
        Share(std::string sym){symbol = sym;}
        std::string getSymbol(){return symbol;}
        void readCsv(std::string filename);
    private:
        std::string symbol;
        std::vector < int > data;

};

#endif
