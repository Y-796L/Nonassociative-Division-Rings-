import time #実行時間出力のためのモジュールをインポート

#原子命題の番号を計算するための関数
def prop_number(n, i, j, k, symbol):
    out = i*(n**2) + j*n + k + 1
    if symbol == 'p':
        return out
    elif symbol == 'm':
        return (n**3) + out
    elif symbol == 'y':
        return 2*(n**3) + out
    else:
        return 'error'

def equal_number(n, i, j):
    out = (n**4) + i + n*j
    return out

def gyro_number(n, i, j, k, l):
    out = (n**5) + i + n*j + (n**2)*k + (n**3)*l
    return out

#以下の関数でMinisat等のSATソルバーに入力できる形式(dimacs標準形)で論理式を自動生成する。

#非可換NAF(左右逆元一致の条件あり)の具体例探索のためのCNF作成スクリプト
def gyro_cnf(n):
    time_start = time.time()
    script = ''
    
    kaigyo = '\n' #改行文字
    space = ' ' #1文字半角スペース
    indent = '    ' #4文字スペースでインデント
    
    script += 'p cnf ' + str(2*(n**5)) + space + str(5*n + 2*(n**2) + 2*(n**3)*(n-1) + n**3 + (n**4)*(n-1) + n + n*(n-1) + 2*(n**5) + n**8 + 2*(n**9) + n**3 + n**6 + 2*(n**7) + n + 2*(n-1) +n**2 + 3*(n**3) + 1) + kaigyo
    
    
    #加法、乗法の単位元及び零元の演算結果を制約条件に反映
    for i in range(n):
        #script += str(prop_number(n, i, 0, i, 'p')) + space + '0' + kaigyo
        script += str(prop_number(n, 0, i, i, 'p')) + space + '0' + kaigyo
        script += str(prop_number(n, 0, i, 0, 'm')) + space + '0' + kaigyo
        script += str(prop_number(n, i, 0, 0, 'm')) + space + '0' + kaigyo
        script += str(prop_number(n, i, 1, i, 'm')) + space + '0' + kaigyo
        script += str(prop_number(n, 1, i, i, 'm')) + space + '0' + kaigyo
    #演算表の1マスにはちょうど一つの数字が入るという条件を記述
    for i in range(n):
        for j in range(n):
            for k in range(n):
                script += str(prop_number(n, i, j, k, 'm')) + space    
            script += '0' + kaigyo

            for k in range(n):
                script += str(prop_number(n, i, j, k, 'p')) + space
            script += '0' + kaigyo
    
            
            #一つのマスに複数の数値が入らないようにする制約
            for k in range(n):
                for l in list(set(range(n)) - set([k])):
                    script += str(-prop_number(n, i, j, k, 'm')) + space + str(-prop_number(n, i, j, l, 'm')) + space + '0' + kaigyo
                    script += str(-prop_number(n, i, j, k, 'p')) + space + str(-prop_number(n, i, j, l, 'p')) + space + '0' + kaigyo
    
    #gyro演算について
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    script += str(gyro_number(n, i, j, k, l)) + space    
                script += '0' + kaigyo
                for l in range(n):
                    for l2 in list(set(range(n)) - set([l])):
                        script += str(gyro_number(n, i, j, k, l)) + space + str(-gyro_number(n, i, j, k, l2)) + space + '0' + kaigyo


    filename = 'Cnf_gyro' + str(n) + '.dimacs'
    with open(filename, mode='w') as f:
        f.write(script)
    script = ''

    #equalについて
    for i in range(n):
        script += str(equal_number(n, i, i))  + space + '0' + kaigyo
        for j in list(set(range(n)) - set([i])):
            script += str(-equal_number(n, i, j))  + space + '0' + kaigyo




    #加法のgyro可換性
    for i in range(n):
        for j in range(n):
            for k1 in range(n):
                for k2 in range(n):
                    for k3 in range(n):
                        script += str(-prop_number(n, i, j, k1, 'p')) + space + str(-prop_number(n, j, i, k2, 'p')) + space + str(-gyro_number(n, i, j, k2, k3)) + space + str(equal_number(n, k2, k3)) + space + '0' + kaigyo

    
    #gyro演算の性質
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    for k1 in range(n):
                        script += str(-gyro_number(n, a, b, c, k1)) + space + str(-gyro_number(n, a, b, d, k1)) + space + str(equal_number(n, c, d)) #ジャイロ自己同型の単射性
                        for k2 in range(n):
                            for k3 in range(n):
                                script += str(-prop_number(n, a, b, k1, 'p')) + space + str(-gyro_number(n, a, b, c, k2)) + space + str(-gyro_number(n, k1,  b, c, k3)) + space + str(equal_number(n, k2,  k3)) + space + '0' + kaigyo
                                for k4 in range(n):
                                    script += str(-prop_number(n, b, c, k1, 'p')) + space + str(-prop_number(n, a, b, k2, 'p')) + space + str(-gyro_number(n, a, b, c, k3)) + space + str(-prop_number(n, a, k1, k4, 'p')) + space + str(prop_number(n, k2, k3, k4, 'p')) + space + '0' + kaigyo
                                    script += str(-prop_number(n, c, d, k1, 'p')) + space + str(-gyro_number(n, a, b, c, k2)) + space + str(-gyro_number(n, a, b, d, k3)) + space + str(-gyro_number(n, a, b, k1, k4)) + str(prop_number(n, k2, k3, k4, 'p')) + space + '0' + kaigyo

    #gyro演算の全射性
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    script += str(gyro_number(n, a, b, d, c)) + space    
            script += '0' + kaigyo

    #乗法の結合則
    for i in range(n):
        for j in range(n):
            for k in range(n):
                with open(filename, mode='a') as f:
                    f.write(script)
                script = ''
                for l1 in range(n):
                    for l2 in range(n):
                        for l3 in range(n):
                            script += str(-prop_number(n, i, j, l1, 'm')) + space + str(-prop_number(n, j, k, l2, 'm')) + space + str(-prop_number(n, l1, k, l3, 'm')) + space + str(prop_number(n, i, l2, l3, 'm')) + space + '0' + kaigyo
                            
    #分配法則
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l1 in range(n):
                    with open(filename, mode='a') as f:
                        f.write(script)
                    script = ''
                    for l2 in range(n):
                        for l3 in range(n):
                            for l4 in range(n):
                                script += str(-prop_number(n, j, k, l1, 'p'))+ space + str(-prop_number(n, i, j, l2, 'm')) + space + str(-prop_number(n, i, k, l3, 'm')) + space + str(-prop_number(n, i, l1, l4, 'm')) + space + str(prop_number(n, l2, l3, l4, 'p')) + space + '0' + kaigyo
                                script += str(-prop_number(n, j, k, l1, 'p'))+ space + str(-prop_number(n, j, i, l2, 'm')) + space + str(-prop_number(n, k, i, l3, 'm')) + space + str(-prop_number(n, l1, i, l4, 'm')) + space + str(prop_number(n, l2, l3, l4, 'p')) + space + '0' + kaigyo
    
    #逆元の存在
    for i in range(n):
        #加法逆元の存在
        for j in range(n):
            script += str(prop_number(n, j, i, 0, 'p')) + space
        script += '0' + kaigyo
        #乗法逆元の存在
        if (i != 0):
            for j in range(n):
                script += str(prop_number(n, i, j, 1, 'm')) + space
            script += '0' + kaigyo
            for j in range(n):
                script += str(prop_number(n, j, i, 1, 'm')) + space
            script += '0' + kaigyo
    
    with open(filename, mode='a') as f:
        f.write(script)
    script = ''
        
    #乗法の右逆元と左逆元の一致
    for i in range(n):
        for j in range(n):
            script += str(-prop_number(n, i, j, 1, 'm')) + space + str(prop_number(n, j, i, 1, 'm')) + space + '0' + kaigyo

    with open(filename, mode='a') as f:
        f.write(script)
    script = ''

    #乗法の非可換性
    for i in range(n):
        for j in range(n):
            for k in range(n):
                script += str(-prop_number(n, i, j, k, 'y')) + space + str(prop_number(n, i, j, k, 'm')) + space + '0' + kaigyo
                script += str(-prop_number(n, i, j, k, 'y')) + space + str(-prop_number(n, j, i, k, 'm')) + space + '0' + kaigyo
                script += str(-prop_number(n, i, j, k, 'm')) + space + str(prop_number(n, j, i, k, 'm')) + space + str(prop_number(n, i, j, k, 'y')) + space + '0' + kaigyo
    for i in range(n):
        for j in range(n):
            for k in range(n):
                script += str(prop_number(n, i, j, k, 'y')) + space
    script += '0' + kaigyo

    with open(filename, mode='a') as f:
        f.write(script)

    
    print('Cnf %d has been written.\n' % n)
    time_execution = time.time() - time_start
    print('Execution time is %f seconds.\n\n' % time_execution)
