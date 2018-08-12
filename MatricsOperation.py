#coding:utf-8
###python中矩阵的相关处理
class Test:


#1:旋转矩阵 —— 顺时针旋转90度，先倒排，再置换
    def transformImage(self, mat, n):
        for i in range(n):
            for j in range(n/2):
                t = mat[j][i]
                mat[j][i] = mat[n-j-1][i]
                mat[n-j-1][i] = t
        print mat
        for i in range(n-1):
            for j in range(i,n):
                t = mat[i][j]
                mat[i][j] = mat[j][i]
                mat[j][i] = t
        return mat

#2:将矩阵汇总含有0的行与列清零，先记录，再清零
    def clearZero(self, mat, n):
        l=[]
        for i in range(n):
            for j in range(n):
                if mat[i][j]==0:
                    l.append((i,j))
        for x,y in l:
            mat[x]=[0]*n
            for i in range(n):
                mat[i][y]=0

        return mat

#3：集合栈 —— 新栈用一个n*size的矩阵表式，一行表示一个单元栈，栈满新建下一个栈（重启一行）
    def setOfStacks(self, ope, size):
        stack =[[]]
        for x in ope:
            if x[0] == 1:
                if len(stack[-1])==size:
                    stack.append([])
                    #栈满，重启一栈，在stack的末尾添加新的空列表[]
                stack[-1].append(x[1])
                #操作数为1：在stack末尾的[]中添加
            if x[0]==2:
                if len(stack[-1])==0:
                    stack.pop()
                    #栈空，删除末尾的空列表
                stack[-1].pop()
                # 操作数为2：删除stack末尾[]中的内容
        return stack





if __name__ == '__main__':
    R=Test()
    #print R.transformImage([[1,2,3],[4,5,6],[7,8,9]],3)
    #print R.clearZero([[1,2,3,0],[1,1,2,0],[0,1,0,1],[2,1,2,1]],4)
    #print R.setOfStacks([[1,2],[2,4],[1,4],[1,5],[2,1],[1,2],[1,3],[1,4]],2)

