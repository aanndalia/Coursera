public class Percolation {
   public Percolation(int N)
   {
	   // create N-by-N grid, with all sites blocked
	   // In Java, 0 is implicit default for integral elements in an array
	   // By convention, we use 0 (False) as blocked and 1 (True) as open
	   grid = new Boolean[N+1][N+1];
	   this.N = N;
	   UF = new WeightedQuickUnionUF(N);
   }
   public void open(int i, int j)
   {
	   if(checkRangeValid(i,j) == false)
	   {
		   throw new java.lang.IndexOutOfBoundsException();
	   }
	   // open site (row i, column j) if it is not already
	   grid[i][j] = true;
	   UF.union(p, q)
	   
   }
   public boolean isOpen(int i, int j)
   {
	   if(checkRangeValid(i,j) == false	)
	   {
		   throw new java.lang.IndexOutOfBoundsException();
	   }
	   // is site (row i, column j) open?
	   return grid[i][j];
   }
   public boolean isFull(int i, int j)
   {
	   // is site (row i, column j) full?
	   return grid[i][j] == false ? true : false;
   }
   public boolean percolates()
   {
	   // does the system percolate?
   }
   private boolean checkRangeValid(int i, int j)
   {
	   if(i < 0 || i >= N || j < 0 || j >= N)
		   return false;
	   else
		   return true;
   }
   
   private Boolean[][] grid; // The grid is an N x N array
   private int N; // The size of the grid
   private WeightedQuickUnionUF UF;
  
	//public static void main(String[] args) {
		// TODO Auto-generated method stub
		//QuickFindUF qf = new QuickFindUF(N);
	//}

}
