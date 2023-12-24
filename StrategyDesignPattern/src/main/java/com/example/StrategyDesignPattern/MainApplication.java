package com.example.StrategyDesignPattern;

import com.example.StrategyDesignPattern.Order.Order;
import com.example.StrategyDesignPattern.strategies.PayByCreditCard;
import com.example.StrategyDesignPattern.strategies.PayByPayPal;
import com.example.StrategyDesignPattern.strategies.PayStrategy;

import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

@SpringBootApplication
public class MainApplication {
    private static final Map<Integer, Integer> priceOnProducts = new HashMap<>();
    private static final BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
    private static final Order order = new Order();
    private static PayStrategy strategy;

    static {
        priceOnProducts.put(1, 2200);
        priceOnProducts.put(2, 1850);
        priceOnProducts.put(3, 1100);
        priceOnProducts.put(4, 890);
    }

    public static void main(String[] args) throws IOException {
        while (!order.isClosed()){
            int cost;

            String continueChoice;
            do {
                System.out.println("Please, select a product:" + "\n" +
                        "1 - Motherboard" + "\n" +
                        "2 - CPU" + "\n" +
                        "3 - RAM" + "\n" +
                        "4 - HDD" + "\n");
                int choice = Integer.parseInt(reader.readLine());
                cost = priceOnProducts.get(choice);
                System.out.println("Count: ");
                int count = Integer.parseInt(reader.readLine());
                order.setTotalCost(cost * count);
                System.out.println("Do you wish to continue selecting products? Y/N: ");
                continueChoice = reader.readLine();
            } while (continueChoice.equalsIgnoreCase("Y"));

            if (strategy == null){
                System.out.println("Please, select a payment method:" + "\n" +
                        "1 - PalPay" + "\n" +
                        "2 - Credit Card");
                String paymentMethod = reader.readLine();

                if (paymentMethod.equals("1")){
                    strategy = new PayByPayPal();
                } else {
                    strategy = new PayByCreditCard();
                }
            }

            order.processOrder(strategy);

            System.out.println("Pay " + order.getTotalCost() + " units or Continue shopping? P/C: ");
            String proceed = reader.readLine();
            if (proceed.equalsIgnoreCase("P")){
                if (strategy.pay(order.getTotalCost())){
                    System.out.println("Payment has been successful.");
                } else {
                    System.out.println("FAIL! Please, check your data.");
                }
                order.setClosed();
            }
        }
    }

}
