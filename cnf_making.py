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

#以下の関数でMinisat等のSATソルバーに入力できる形式(dimacs標準形)で論理式を自動生成する。

#非可換NAF(左右逆元一致の条件あり)の具体例探索のためのCNF作成スクリプト
def cnf_making(n):
    time_start = time.time()
    script = ''
    
    kaigyo = '\n' #改行文字
    space = ' ' #1文字半角スペース
    indent = '    ' #4文字スペースでインデント
    
    script += 'p cnf ' + str(3*(n**3)) + space + str(6*n + 2*(n**2) + 2*(n**3)*(n-1) + n**3 + n**6 + 2*(n**7) + n + 2*(n-1) +n**2 + 3*(n**3) + 1) + kaigyo
    
    
    #加法、乗法の単位元及び零元の演算結果を制約条件に反映
    for i in range(n):
        script += str(prop_number(n, i, 0, i, 'p')) + space + '0' + kaigyo
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
    
    filename = 'Cnf' + str(n) + '.dimacs'
    with open(filename, mode='w') as f:
        f.write(script)
    script = ''


    #加法の可換性
    for i in range(n):
        for j in range(n):
            for k in range(n):
                script += str(-prop_number(n, i, j, k, 'p')) + space + str(prop_number(n, j, i, k, 'p')) + space + '0' + kaigyo


    #加法の結合測
    for i in range(n):
        for j in range(n):
            for k in range(n):
                with open(filename, mode='a') as f:
                    f.write(script)
                script = ''
                for l1 in range(n):
                    for l2 in range(n):
                        for l3 in range(n):
                            script += str(-prop_number(n, i, j, l1, 'p')) + space + str(-prop_number(n, j, k, l2, 'p')) + space + str(-prop_number(n, l1, k, l3, 'p')) + space + str(prop_number(n, i, l2, l3, 'p')) + space + '0' + kaigyo
                            
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
            script += str(prop_number(n, i, j, 0, 'p')) + space
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


#Semifieldの具体例探索のためのCNF作成スクリプト
def cnf_semifield(n):
    time_start = time.time()
    script = ''
    
    kaigyo = '\n' #改行文字
    space = ' ' #1文字半角スペース
    indent = '    ' #4文字スペースでインデント
    
    script += 'p cnf ' + str(3*(n**3)) + space + str(6*n+2*(n**2)+2*(n**3)*(n-1)+n**3+n**6+2*(n**7)+n+n**2+3*(n**3)+1) + kaigyo
    
    
    #加法、乗法の単位元及び零元の演算結果を制約条件に反映
    for i in range(n):
        script += str(prop_number(n, i, 0, i, 'p')) + space + '0' + kaigyo
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
    
    filename = 'Semifield' + str(n) + '.dimacs'
    with open(filename, mode='w') as f:
        f.write(script)
    script = ''


    #加法の可換性
    for i in range(n):
        for j in range(n):
            for k in range(n):
                script += str(-prop_number(n, i, j, k, 'p')) + space + str(prop_number(n, j, i, k, 'p')) + space + '0' + kaigyo


    #加法の結合測
    for i in range(n):
        for j in range(n):
            for k in range(n):
                with open(filename, mode='a') as f:
                    f.write(script)
                script = ''
                for l1 in range(n):
                    for l2 in range(n):
                        for l3 in range(n):
                            script += str(-prop_number(n, i, j, l1, 'p')) + space + str(-prop_number(n, j, k, l2, 'p')) + space + str(-prop_number(n, l1, k, l3, 'p')) + space + str(prop_number(n, i, l2, l3, 'p')) + space + '0' + kaigyo
                            
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
            script += str(prop_number(n, i, j, 0, 'p')) + space
        script += '0' + kaigyo
    

    with open(filename, mode='a') as f:
        f.write(script)
    script = ''

    #零因子が0のみであること
    for i in range(n):
        for j in range(n):
            script += str(-prop_number(n, i, j, 0, 'm')) + space + str(prop_number(n, i, 0, 0, 'p')) + space + str(prop_number(n, j, 0, 0, 'p')) + space + '0' + kaigyo


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

#加法交換律を緩める
def cnf_making_kahou(n):
    time_start = time.time()
    script = ''
    
    kaigyo = '\n' #改行文字
    space = ' ' #1文字半角スペース
    indent = '    ' #4文字スペースでインデント
    
    script += 'p cnf ' + str(3*(n**3)) + space + str(6*n + 2*(n**2) + 2*(n**3)*(n-1) + n**3 + n**6 + 2*(n**7) + n + 2*(n-1)  + 3*(n**3) + 1 - n**3) + kaigyo
    
    
    #加法、乗法の単位元及び零元の演算結果を制約条件に反映
    for i in range(n):
        script += str(prop_number(n, i, 0, i, 'p')) + space + '0' + kaigyo
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
    
    filename = 'Cnf_kahou' + str(n) + '.dimacs'
    with open(filename, mode='w') as f:
        f.write(script)
    script = ''


    #加法の可換性
    #for i in range(n):
        #for j in range(n):
            #for k in range(n):
                #script += str(-prop_number(n, i, j, k, 'p')) + space + str(prop_number(n, j, i, k, 'p')) + space + '0' + kaigyo


    #加法の結合測
    for i in range(n):
        for j in range(n):
            for k in range(n):
                with open(filename, mode='a') as f:
                    f.write(script)
                script = ''
                for l1 in range(n):
                    for l2 in range(n):
                        for l3 in range(n):
                            script += str(-prop_number(n, i, j, l1, 'p')) + space + str(-prop_number(n, j, k, l2, 'p')) + space + str(-prop_number(n, l1, k, l3, 'p')) + space + str(prop_number(n, i, l2, l3, 'p')) + space + '0' + kaigyo
                            
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
            script += str(prop_number(n, i, j, 0, 'p')) + space
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
    #for i in range(n):
        #for j in range(n):
            #script += str(-prop_number(n, i, j, 1, 'm')) + space + str(prop_number(n, j, i, 1, 'm')) + space + '0' + kaigyo

    #with open(filename, mode='a') as f:
        #f.write(script)
    #script = ''

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

#加法交換律および結合律を緩める
def cnf_making_addketu(n):
    time_start = time.time()
    script = ''
    
    kaigyo = '\n' #改行文字
    space = ' ' #1文字半角スペース
    indent = '    ' #4文字スペースでインデント
    
    script += 'p cnf ' + str(3*(n**3)) + space + str(6*n + 2*(n**2) + 2*(n**3)*(n-1) + n**3 + 2*(n**7) + n + 2*(n-1)  + 3*(n**3) + 1 - n**3) + kaigyo
    
    
    #加法、乗法の単位元及び零元の演算結果を制約条件に反映
    for i in range(n):
        script += str(prop_number(n, i, 0, i, 'p')) + space + '0' + kaigyo
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
    
    filename = 'Cnf_addketu' + str(n) + '.dimacs'
    with open(filename, mode='w') as f:
        f.write(script)
    script = ''


    #加法の可換性
    #for i in range(n):
        #for j in range(n):
            #for k in range(n):
                #script += str(-prop_number(n, i, j, k, 'p')) + space + str(prop_number(n, j, i, k, 'p')) + space + '0' + kaigyo


    #加法の結合測
    #for i in range(n):
        #for j in range(n):
            #for k in range(n):
                #with open(filename, mode='a') as f:
                    #f.write(script)
                #script = ''
                #for l1 in range(n):
                    #for l2 in range(n):
                        #for l3 in range(n):
                            #script += str(-prop_number(n, i, j, l1, 'p')) + space + str(-prop_number(n, j, k, l2, 'p')) + space + str(-prop_number(n, l1, k, l3, 'p')) + space + str(prop_number(n, i, l2, l3, 'p')) + space + '0' + kaigyo
                            
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
            script += str(prop_number(n, i, j, 0, 'p')) + space
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
    #for i in range(n):
        #for j in range(n):
            #script += str(-prop_number(n, i, j, 1, 'm')) + space + str(prop_number(n, j, i, 1, 'm')) + space + '0' + kaigyo

    #with open(filename, mode='a') as f:
        #f.write(script)
    #script = ''

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


#左右逆元一致の条件なし
def cnf_making_WIC(n):
    time_start = time.time()
    script = ''
    
    kaigyo = '\n' #改行文字
    space = ' ' #1文字半角スペース
    indent = '    ' #4文字スペースでインデント
    
    script += 'p cnf ' + str(3*(n**3)) + space + str(6*n + 2*(n**2) + 2*(n**3)*(n-1) + n**3 + n**6 + 2*(n**7) + n + 2*(n-1)  + 3*(n**3) + 1) + kaigyo
    
    
    #加法、乗法の単位元及び零元の演算結果を制約条件に反映
    for i in range(n):
        script += str(prop_number(n, i, 0, i, 'p')) + space + '0' + kaigyo
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
    
    filename = 'Cnf_WIC' + str(n) + '.dimacs'
    with open(filename, mode='w') as f:
        f.write(script)
    script = ''


    #加法の可換性
    for i in range(n):
        for j in range(n):
            for k in range(n):
                script += str(-prop_number(n, i, j, k, 'p')) + space + str(prop_number(n, j, i, k, 'p')) + space + '0' + kaigyo


    #加法の結合測
    for i in range(n):
        for j in range(n):
            for k in range(n):
                with open(filename, mode='a') as f:
                    f.write(script)
                script = ''
                for l1 in range(n):
                    for l2 in range(n):
                        for l3 in range(n):
                            script += str(-prop_number(n, i, j, l1, 'p')) + space + str(-prop_number(n, j, k, l2, 'p')) + space + str(-prop_number(n, l1, k, l3, 'p')) + space + str(prop_number(n, i, l2, l3, 'p')) + space + '0' + kaigyo
                            
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
            script += str(prop_number(n, i, j, 0, 'p')) + space
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
    #for i in range(n):
        #for j in range(n):
            #script += str(-prop_number(n, i, j, 1, 'm')) + space + str(prop_number(n, j, i, 1, 'm')) + space + '0' + kaigyo

    #with open(filename, mode='a') as f:
        #f.write(script)
    #script = ''

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



#テスト用(可換体も検出する)
def test(n):
    time_start = time.time()
    script = ''
    
    kaigyo = '\n' #改行文字
    space = ' ' #1文字半角スペース
    indent = '    ' #4文字スペースでインデント
    
    script += 'p cnf ' + str(3*(n**3)) + space + str(6*n + 2*(n**2) + 2*(n**3)*(n-1) + n**3 + n**6 + 2*(n**7) + n + 2*(n-1)) + kaigyo
    
    
    #加法、乗法の単位元及び零元の演算結果を制約条件に反映
    for i in range(n):
        script += str(prop_number(n, i, 0, i, 'p')) + space + '0' + kaigyo
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
    
    filename = 'Cnf_test' + str(n) + '.dimacs'
    with open(filename, mode='w') as f:
        f.write(script)
    script = ''


    #加法の可換性
    for i in range(n):
        for j in range(n):
            for k in range(n):
                script += str(-prop_number(n, i, j, k, 'p')) + space + str(prop_number(n, j, i, k, 'p')) + space + '0' + kaigyo


    #加法の結合測
    for i in range(n):
        for j in range(n):
            for k in range(n):
                with open(filename, mode='a') as f:
                    f.write(script)
                script = ''
                for l1 in range(n):
                    for l2 in range(n):
                        for l3 in range(n):
                            script += str(-prop_number(n, i, j, l1, 'p')) + space + str(-prop_number(n, j, k, l2, 'p')) + space + str(-prop_number(n, l1, k, l3, 'p')) + space + str(prop_number(n, i, l2, l3, 'p')) + space + '0' + kaigyo
                            
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
            script += str(prop_number(n, i, j, 0, 'p')) + space
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
    #for i in range(n):
        #for j in range(n):
            #script += str(-prop_number(n, i, j, 1, 'm')) + space + str(prop_number(n, j, i, 1, 'm')) + space + '0' + kaigyo

    #with open(filename, mode='a') as f:
        #f.write(script)
    #script = ''

    #乗法の非可換性
    #for i in range(n):
        #for j in range(n):
            #for k in range(n):
                #script += str(-prop_number(n, i, j, k, 'y')) + space + str(prop_number(n, i, j, k, 'm')) + space + '0' + kaigyo
                #script += str(-prop_number(n, i, j, k, 'y')) + space + str(-prop_number(n, j, i, k, 'm')) + space + '0' + kaigyo
                #script += str(-prop_number(n, i, j, k, 'm')) + space + str(prop_number(n, j, i, k, 'm')) + space + str(prop_number(n, i, j, k, 'y')) + space + '0' + kaigyo
    #for i in range(n):
        #for j in range(n):
            #for k in range(n):
                #script += str(prop_number(n, i, j, k, 'y')) + space
    #script += '0' + kaigyo

    with open(filename, mode='a') as f:
        f.write(script)

    
    print('Cnf %d has been written.\n' % n)
    time_execution = time.time() - time_start
    print('Execution time is %f seconds.\n\n' % time_execution)