#include <iostream> // std::cout, std::endl, std::cerr
#include <fstream> // std::ifstream
#include <vector> // std::vector
#include <cstdlib> // std::exit
#include <sstream> // std::stringstream
#include <string> // std::string, std::stoi
#include <utility> // std::pair

std::vector<int>
convert(std::vector<std::string> v)
{
    std::vector<int> result;
    for (std::string s : v) {
        result.push_back(std::stoi(s));
    }
    return result;
}

const std::vector<std::string>
split(const std::string &s, const char &c)
{
    std::string buff{""};
    std::vector<std::string> v;

    for (auto n : s) {
        if (n != c) {
            buff += n;
        } else if (n == c && buff != "") {
            v.push_back(buff);
            buff = "";
        }
    }
    if (buff != "") {
        v.push_back(buff);
    }
    return v;
}

std::vector<std::vector<int>>
convert_program(std::string program, int arg1, int arg2)
{
    std::vector<std::vector<int>> table;
    std::vector<std::string> data{ split(program, ',')};
    while (!(data.size() < 4)) {
        std::vector<int> v = convert({data[0], data[1], data[2], data[3]});
        table.push_back(v);
        data.erase(data.begin(), data.begin() + 4);
    }
    std::vector<int> v;
    for (std::string s : data) {
        v.push_back(std::stoi(s));
    }
    table.push_back(v);
    table[0][1] = arg1; table[0][2] = arg2;
    return table;
}

template <typename T>
std::vector<T> flatten(const std::vector<std::vector<T>> &vec) {   
    std::vector<T> result;
    for (const auto &v : vec)
        result.insert(result.end(), v.begin(), v.end());                                                                                         
    return result;
}

std::vector<int>
run(std::vector<std::vector<int>> &program)
{
    std::vector<int> prog = flatten(program);
    for (std::vector<int> dir : program) {
        switch (dir[0]) {
            case 1: 
                prog[dir[3]] = prog[dir[1]] + prog[dir[2]];
                break;
            case 2:
                prog[dir[3]] = prog[dir[1]] * prog[dir[2]];
                break;
            default:
                return prog;
        }
    }
    return prog;
}

std::pair<int, int>*
values_that_produce(int terminal, std::string data)
{
    std::pair<int, int> *result;
    for (int i = 0; i < 100; ++i) {
        for (int j = 0; j < 100; ++j) {
            std::vector<std::vector<int>> converted = convert_program(data, i, j);
            std::vector<int> intcode = run(converted);
            if (intcode[0] == terminal) {
                result->first = i; result->second = j;
                return result;
            }
        }
    }
    return nullptr;
}

int 
main(int argc, char const *argv[])
{
    int terminal = 19690720;
    if (argc > 1) {
        std::stringstream convert(argv[1]);
        if (!(convert >> terminal)) {
            terminal = 19690720;
        }
    }

    std::ifstream input("input.txt");
    if (!input) {
        std::cerr << "'input.txt' was not found" << std::endl;
        std::exit(1);
    }
    std::string data;
    getline(input, data);

    std::pair<int, int> *result = values_that_produce(terminal, data);
    if (result) {
        std::cout << "x: " << result->first << " y: " << result->second << std::endl;
        std::cout << (((result->first) * 100) + (result->second)) << std::endl;
    } else {
        std::cout << "No combination exists" << std::endl;
    }

    return 0;
}
