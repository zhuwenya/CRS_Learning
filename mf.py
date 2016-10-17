import tensorflow as tf


INFINITY=10e+12

class TF(object):
    def __init__(self,config):
        self.User_Item_Matrix=tf.constant(config.User_Item_Matrix,dtype=tf.float32)
        self.rank=config.rank
        self.lr=config.lr
        self.max_iter=config.max_iter
        self.min_delta=config.min_delta
        Matrix_Shape=config.User_Item_Matrix.shape

        scale=2*np.sqrt(config.User_Item_Matrix.mean()/rank)
        initializer=tf.random_uniform_initializer(maxval=scale)

        # define the hidden vector we should learn as the variable (W represent the user hidden matrix and H represents the item hideen matrix)
        self.H=tf.get_variable("H",[rank,shape[1]],initializer=initializer)
        self.W=tf.get_variable("W",[shape[0],rank],initializer=initializer)

        self._build_grad_algorithm()

    def _build_grad_algorithm(self):
        """ build dataflow graph for optimization with adagrad algorithm"""
        User_Item_Matrix,H,W= self.User_Item_Matrix,self.H,self.W
        WH=tf.matmul(W,H)

        #the cost of the matrix rescontruction
        f_norm=tf.reduce_sum(tf.pow(User_Item_Matrix-WH,2))

        #non-negative constraint
        #if all elments are positive, constraint will be 0
        nn_w=tf.reduce_sum(tf.abs(W)-W)
        nn_h=tf.reduce_sum(tf.abs(H)-H)
        constraint=INFINITY*(nn_w+nn_h)

        self.loss=loss=f_norm+constraint
        self.optimize=tf.train.AdagradOptimizer(self.lr).minimize(loss)

    def _run_grad(self,sess):
        pre_loss=INFINITY
        for i in xrange(self.max_iter):
            loss,_=sess.run([self.loss,self.optimize])
            if pre_loss-loss<self.min_delta:
                break
            pre_loss=loss
        W=self.W.eval()
        H=self.H.eval()
        return W,H
