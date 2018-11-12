import random
import sys


MS_SIZE = 8          # ゲームボードのサイズ
CLOSE, OPEN, FLAG = 0, 1, 2

class Game:

    def __init__(self, number_of_mines = 10):
        """ ゲームボードの初期化

        Arguments:
        number_of_mines -- 地雷の数のデフォルト値は10

        Side effects:
        mine_map[][] -- 地雷マップ(-1: 地雷，>=0 8近傍の地雷数)
        game_board[][] -- 盤面 (0: CLOSE(初期状態), 1: 開いた状態, 2: フラグ)

        """

        self.init_game_board()
        self.init_mine_map(number_of_mines)
        self.count_mines()

    def init_game_board(self):
        """ ゲーム盤を初期化 """
        # <-- (STEP 1) ここにコードを追加       
        #0を代入
        self.game_board = [[0 for j in range(MS_SIZE)] for i in range(MS_SIZE)]

    def init_mine_map(self, number_of_mines):
        """ 地雷マップ(self->mine_map)の初期化
        Arguments:
        number_of_mines -- 地雷の数
        
        地雷セルに-1を設定する．      
        """
        # <-- (STEP 2) ここにコードを追加

        #self.mine_mapの全ての要素に0を入れる
        self.mine_map = [[0 for i in range(MS_SIZE)] for j in range(MS_SIZE)]
        
        #is_finishedでもnumber_of_minesを使用したいのでインスタンス変数にいれておく
        if number_of_mines < 0 :
            self.f_mines = 0
        elif number_of_mines > MS_SIZE * MS_SIZE :
            number_of_mines = MS_SIZE * MS_SIZE
        else:
            self.f_mines = number_of_mines
        
        #number_of minesが負の数かであれば何もしない
        if number_of_mines < 0 :
            return 


       #number_of_minesの数だけ-1をmine_mapに入れる 
        mine_count = 0
        #print(number_of_mines)
        if number_of_mines < 0:
            pass
        else:
            while True :
                x = random.randint(0,MS_SIZE-1)
                y = random.randint(0,MS_SIZE-1)
                if self.mine_map[x][y] == 0 :
                    self.mine_map[x][y] = -1
                    mine_count += 1
                if mine_count == number_of_mines :
                    break

    def count_mines(self):
        """ 8近傍の地雷数をカウントしmine_mapに格納 
        地雷数をmine_map[][]に設定する．
        """
        # <-- (STEP 3) ここにコードを追加
        #全てのセルを見るのではなく、爆弾が入っているセルの周り8つのセルに爆弾の数を入れて行く方法をとる
        for i in range(MS_SIZE):
            for j in range(MS_SIZE):
                if self.mine_map[i][j] == -1:
                   for k in range(-1,2) :
                       for l in range(-1,2):
                           #存在しない要素にアクセスするときはpass
                           if i + k < 0 or i + k > 7 or j + l < 0 or j + l > 7 :
                               pass
                           #調べる中心はpass
                           elif k == 0 and l == 0 :
                               pass
                           #セルに爆弾が入っていればカウントしない
                           elif self.mine_map[i + k][j + l] == -1:
                               pass
                           #最後に何もないセルにカウントする
                           else:
                               self.mine_map[i + k][j + l] += 1

    
    def open_cell(self, x, y):
        """ セル(x, y)を開ける
        Arguments:
        x, y -- セルの位置
        
        Returns:
          True  -- 8近傍セルをOPENに設定．
                   ただし，地雷セル，FLAGが設定されたセルは開けない．    
          False -- 地雷があるセルを開けてしまった場合（ゲームオーバ）
        
        """
        # <-- (STEP 4) ここにコードを追加
        if self.mine_map[y][x] == -1:
            return False
        else:
            for i in range(-1, 2):
                for j in range(-1,2):
                    #存在しないセルにアクセスしようとしたらpass
                    if x + j < 0 or x + j > 7 or y + i < 0 or y + i > 7:
                        pass
                    #８近傍のうち爆弾があればpass
                    elif self.mine_map[y + i][x + j] == -1 :
                        pass
                    else:
                        #指定したセルはフラグの有無にかかわらず開けるので、まず開けてしまう
                        self.game_board[y][x] = 1
                        #フラグが８近傍にあれば開けない
                        if self.game_board[y + i][x + j] != 2 :  #フラグでないなら開ける
                            self.game_board[y + i][x + j] = 1
                        elif self.game_board[y + i][x + j] == 2 :   #フラグがあれば何もしない
                            pass
            return True
    
    def flag_cell(self, x, y):
        """
        セル(x, y)にフラグを設定する，既に設定されている場合はCLOSE状態にする
        """
        # <-- (STEP 5) ここにコードを追加
        #すでに空いているセルなら何もしない
        if self.game_board[y][x] == 1:
            pass
        #フラグがすでに立っているセルだったなら、フラグを除去する
        elif self.game_board[y][x] == 2:
            self.game_board[y][x] = 0
        #相手いないセルならフラグを立てる
        else:
            self.game_board[y][x] = 2

    def is_finished(self):
        """ 地雷セル以外のすべてのセルが開かれたかチェック """
        # <-- (STEP 6) ここにコードを追加
        count_f_cells = 0
        #空いていないセルの数と地雷の数が同じであればゲームクリアになる
        for i in range(MS_SIZE):
            for j in range(MS_SIZE):
                #空いていないセルの数をカウントする
                if self.game_board[i][j] == 0 or self.game_board[i][j] == 2:
                    count_f_cells += 1

        #爆弾の数を数える
        mines = 0
        for i in range(MS_SIZE) :
            for j in range(MS_SIZE) :
                if self.mine_map[i][j] == -1 :
                    mines += 1
        
        if count_f_cells == mines :
            return True
        else :
            return False

        
    def print_header(self):
        print("=====================================")
        print("===  Mine Sweeper Python Ver. 1  ====")
        print("=====================================")

    def print_footer(self):
        print("   ", end="")
        for x in range(MS_SIZE):
            print("---", end="")
        print("[x]\n   ", end="")
        for x in range(MS_SIZE):
            print("%3d"%x, end="")
        print("")
        
    def print_mine_map(self):
        print(" [y]")
        for y in range(MS_SIZE):
            print("%2d|"%y, end="")
            for x in range(MS_SIZE):
                print("%2d"%self.mine_map[y][x], end="")
            print("")
        
    def print_game_board(self):
        marks = ['x', ' ', 'P']
        self.print_header()
        print("[y]")
        for y in range(MS_SIZE):
            print("%2d|"%y, end="")
            for x in range(MS_SIZE):
                if self.game_board[y][x] == OPEN and self.mine_map[y][x] > 0:
                    print("%3d"%self.mine_map[y][x], end="")
                else:
                    print("%3s"%marks[self.game_board[y][x]], end="")
            print("")
        self.print_footer()

if __name__ == '__main__':
    b = Game()
    quitGame = False
    while not quitGame:
        b.print_game_board()
        print("o x y: セルを開く，f x y: フラグ設定/解除, q: 終了 -->", end="")
        command_str = input()

        try:
            cmd = command_str.split(" ")
            if cmd[0] == 'o':
                x, y = cmd[1:]
                if b.open_cell(int(x), int(y)) == False:
                    print("ゲームオーバー!")
                    quitGame = True
            elif cmd[0] == 'f':
                x, y = cmd[1:]
                b.flag_cell(int(x), int(y))
            elif cmd[0] == 'q':
                print("ゲームを終了します．")
                quitGame = True
                break
            else:
                print("コマンドはo, f, qのいずれかを指定してください．")
        except:
            print("もう一度，コマンドを入力してください．")
            
        if b.is_finished():
            b.print_game_board()
            print("ゲームクリア!")
            quitGame = True
