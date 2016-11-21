#include "share.h"

/*read full csv file stored in datastore*/
void Share::readCsv(std::string filename, int show){
    std::ifstream in;
    std::vector<std::string> row;
    std::vector<std::string> split_string;
    std::string line;
    std::string tok;
    std::string s;
    in.open(filename.c_str());
    /*read in each line as full string*/
    while(std::getline(in, line)){
        row.push_back(line);
        if (show){
            std::cout<<line<<std::endl;
        }
    }
    /*parse each string after in memory - assumes strict csv file format*/
    for(std::vector<std::string>::iterator it=row.begin(); it!=row.end(); ++it){
        std::stringstream ss(*it);
        while(getline(ss, tok, ',')){
            split_string.push_back(tok);
        }
        data.push_back(split_string);
        split_string.clear();
    }
}

/*format string matrix data to symbol_data type*/
void Share::formatData(){
    for(str_matrix::iterator it=data.begin(); it!=data.end(); ++it){
        fdata.push_back(Entry(*it));
    }
}

/*str_matrix data type for each symbol - print to stdout*/
void Share::showData(){
    for(str_matrix::iterator it=data.begin(); it!=data.end(); ++it){
        for(std::vector<std::string>::iterator s=it->begin(); s!=it->end(); ++s){
            std::cout<<*s<<" ";
        }
        std::cout<<std::endl;
    }
}


