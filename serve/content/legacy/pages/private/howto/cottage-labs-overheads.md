# How to do Cottage Labs overheads

What you will need:

Login to Open Books, open two browser windows for:
* Invoices Window
* Bills Window

## Step 0:

Locate the most recent invoice for which an overhead has not already been raised.

This should be the invoice whose raised date is the next one after the last raised date of an overhead payment

## Step 1:

Take note of:
* the invoice number
* the invoice amount *excluding* VAT
* which project the invoice came from


## Step 2:
In the bills window, create a new bill with the following fields 

Supplier Contact: Cottage Labs (internal)
Reference: Cottage Labs Overheads - Invoice [invoice number]
Total Value: 10% of ex-VAT invoice value
Category: Cottage Labs Overheads
Comments: [copy Reference]

Link to project: [the project being paid]

then Create and Finish

## Step 3

Pay the Bill

Banking -> Overhead Contra Account -> More -> Add Transaction

Type: Bill Payment
Amount: overhead amount (i.e. 10% of the ex VAT invoice)
Bill: choose the bill created in Step 2

then Create and Finish

 ## Step 4

Refund the overhead contra account
(very important, so we aren't fiddling the books by accident!)

Banking -> Overhead Contra Account -> More -> Add Transaction

Type: Refund

Date: today
Total Amount: same as refund amount
Category: Cottage Labs Overheads
Description: Overheads refund - Invoice [invoice number]

Link to project: Cottage Labs (internal): CL Overheads

then Create and Finish

## Step 5

Check that the balance of the Overhead Contra Account == 0

There should be two transactions for the project, one with money out and one with money in, with equivalent values

Check that the project has the bill associated with it:
Work -> Projects -> [the project] -> Expenses
And check that the bill shows up

Check that the CL Overheads project has the refund associated with it:
Work -> Projects -> CL Overheads -> Expenses
And check that the refund shows up







Original Title: How to do Cottage Labs Overheads
Original Author: richard
Tags: howto
Created: 2013-12-22 1043
Last Modified: 2014-06-03 2009
