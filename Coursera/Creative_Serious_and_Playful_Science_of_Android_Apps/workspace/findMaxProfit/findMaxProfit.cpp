/*
 * findMaxProfit.cpp
 *
 *  Created on: Feb 15, 2014
 *      Author: Andrew_Dalia
 */

#include <iostream>
#include <string>
#include <stdlib.h>

int main()
{
	int arr[] = {100, 50, 125, 150, 25, 75};
	const int NUM = 6;

	int maxProfit = 0;
	int buyPrice = arr[0];
	int sellPrice = 0;
	int buyIndex = 0;
	int sellIndex = 0;

	for(int i=1; i < NUM ; i++)
	{
		if(arr[i] < buyPrice)
		{
			buyPrice = arr[i];
		}
		else if(arr[i] > sellPrice)
		{
			sellPrice = arr[i];
			if((sellPrice - buyPrice) > maxProfit )
			{
				maxProfit = sellPrice - buyPrice;
			}
		}
	}

	std::cout << "max profit is " << maxProfit << std::endl;
}






