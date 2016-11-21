#include "headers.h"
#include "entry.h"

Entry::Entry(std::vector<std::string > row){
    std::string date="";
    for(int i=0; i<4; i++){
        date+=row[0][i];    
    }
    year = atoi(date.c_str());
    date.clear();
    for(int i=4; i<6; i++){
        date+=row[0][i];    
    }
    month = atoi(date.c_str());
    date.clear();
    for(int i=6; i<8; i++){
        date+=row[0][i];    
    }
    day = atoi(date.c_str());
    adj_close = atof(row[1].c_str());
    close = atof(row[2].c_str());
    high = atof(row[3].c_str());
    low = atof(row[4].c_str());
    open = atof(row[5].c_str());
    symbol = row[6];
    volume = atof(row[7].c_str());

}
