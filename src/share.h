#ifndef SHARE_H_
#define SHARE_H_

#include "entry.h"
#include "headers.h"
/*str_matrix vector of vectors to help read from csv data*/
typedef std::vector<std::vector<std::string> > str_matrix;
/*symbol_data vector of entries formatted for mathy use*/
typedef std::vector< Entry > symbol_data;
/*Share class - will store data pertaining to a particular symbol */
class Share{
    public:
        Share(std::string sym){symbol = sym;}
        std::string getSymbol(){return symbol;}
        /*read csv symbol data, store in str_matrix for further manipulation*/
        void readCsv(std::string filename, int show=0);
        void formatData();
        void showData();
    private:
        std::string symbol;
        std::vector<std::vector<std::string> > data;
        std::vector<Entry> fdata;

};


#endif
