#include <bits/stdc++.h>

using namespace std;
#define int long long
bool sorter(pair<int,float> f, pair<int, float> s) {
    if (f.second>s.second) return true;
    else return false;
}
int32_t main()
{
    int n, k;
    cin >> n >> k;
    vector <float> b;
    for (int i =0; i < n; i++) {
        float tmp;
        cin >> tmp;
        b.push_back(tmp);
    }
    vector <float> c;
    for (int i = 0; i < n; i++) {
        float tmp;
        cin >> tmp;
        c.push_back(tmp);
    }
    vector <pair<int, float>> fsort;
    for (int i = 0 ; i < n; i++) {
        fsort.push_back({i, b[i]/c[i]});
    }
    sort(fsort.begin(), fsort.end(), sorter);
    set <int> ans;
    for (int i = 0; i < k; i++) {
        ans.insert(fsort[i].first+1);
    }
    for (auto el: ans) {
        cout << el << ' ';
    }
}