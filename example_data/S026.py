#include<bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>

#define sz(a) (int)a.size()
#define pb push_back
#define all(a) a.begin(), a.end()
#define for0(i, n) for(int i = 0; i < n; i++)
#define for1(i, n) for(int i = 1; i <= n; i++)
#define x first
#define y second
#define int long long

using namespace std;
using namespace __gnu_pbds;

typedef long long ll;
typedef pair<int, int> pii;
typedef vector<int> vi;
typedef vector<vector<int> > vvi;
typedef tree<pii, null_type, less<pii>, rb_tree_tag, tree_order_statistics_node_update> ordered_set;
typedef map<string, int> msi;

const int inf = 1e18;
const int M = 1e9 + 7;

int n, m;
int dx[4] = {-1, 0, 1, 0};
int dy[4] = {0, 1, 0, -1};

bool inside(int x, int y){
    return (x >= 0 && y >= 0 && x < n && y < m);
}

signed main(){
    //ifstream cin("input.txt");
    //ofstream cout("output.txt");
       ios::sync_with_stdio(0), cin.tie(0), cout.tie(0);


    cin >> n >> m;
    vector<string> S(n);
    for0(i, n){
        cin >> S[i];
    }
    pii st, fin;
    for0(i, n)
        for0(j, m){
            if(S[i][j] == 'S'){
                st = {i, j};
                S[i][j] = '.';
            }
            if(S[i][j] == 'F'){
                fin = {i, j};
                S[i][j] = '.';
            }
        }

    deque<pii> que;
    vvi rev_dir(n, vi(m, -1));
    que.pb(st);
    rev_dir[st.x][st.y] = 4;
    while(sz(que) > 0){
        pii top = que[0];
        que.pop_front();

        for0(i, 4){
            int nx = top.x + dx[i];
            int ny = top.y + dy[i];

            if(inside(nx, ny) && S[nx][ny] == '.' && rev_dir[nx][ny] == -1){
               rev_dir[nx][ny] = (i + 2) % 4;
               que.pb({nx, ny});
            }
        }
    }

    pii t = fin;
    vvi dir(n, vi(m, -1));
    while(t != st){
        pii nt = {t.x + dx[rev_dir[t.x][t.y]], t.y + dy[rev_dir[t.x][t.y]]};
        dir[nt.x][nt.y] = (rev_dir[t.x][t.y] + 2) % 4;
        t = nt;
    }

   int tdir = 2;
   t = st;
   while(dir[t.x][t.y] > -1){
        while(tdir != dir[t.x][t.y]){
            cout << "MOVE RIGHT\n";
            (tdir += 1) %= 4;
        }
        cout << "GO\n";
        t = {t.x + dx[dir[t.x][t.y]], t.y + dy[dir[t.x][t.y]]};
   }
   cout << "FINISH\n";

}