#ifndef SHARE_H_
#define SHARE_H_

#include "headers.h"

class Share{
    public:
        Share(std::string sym){symbol = sym;}
        std::string getSymbol(){return symbol;}
        void readCsv(std::string filename, int show=0);
        void showData();
    private:
        std::string symbol;
        str_matrix data;

};

#endif
