#ifndef ENTRY_H_
#define ENTRY_H
#include <stdlib.h>
#include <iostream>
#include <sqlite3.h>
#include <algorithm>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>

class Entry{
    public:
        Entry(std::vector<std::string > row);
    private:
        int year;
        int month;
        int day;
        int hour;
        int min;
        std::string symbol;
        float volume;
        float adj_close;
        float close;
        float high;
        float low;
        float open;

};

#endif
