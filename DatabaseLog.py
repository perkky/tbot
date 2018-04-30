
# Start of Function ============================================================
def Write_ClayLog( Dateofposition, OpeningPosition, EMA1, EMA2 ):
    #    Setup these fields for table insert
    #    Dateofposition = '2018-04-10 08:09:10'
    #    OpeningPosition = 662.36
    #    EMA1 = 657.17
    #    EMA2 = 649.61
    #    Two fields are returned;
    #    WriteStatus return codes are 'OK-W', 'FAIL', 'DUPE'
    #    ErrorDesc is a description of the error

    WriteStatus = ' '
    ErrorDesc = '   '
    import mysql.connector
    from mysql.connector import errorcode

    # Connect to database
    try:
        db = mysql.connector.connect(user='Clay_User', password='Clay_User',host='192.168.0.26',database='Clay')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            #print("Invalid user name or password")
            ErrorDesc = Dateofposition+' Invalid user name or password'
            WriteStatus = "FAIL"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            #print("Database not found")
            ErrorDesc = Dateofposition+' Database not found'
            WriteStatus = "FAIL"
        else:
            #print(err)
            ErrorDesc = Dateofposition+' Unknown error'
            WriteStatus = "FAIL"
        #endif
    else:
        # No Exceptions then connection is good
        # so lets write to database table
        cursor = db.cursor()
        args = [Dateofposition,OpeningPosition,EMA1,EMA2,WriteStatus]
        # Call database stored procedure to insert record
        # return codes are 'OK-W', 'FAIL', 'DUPE'
        try:
            result_args = cursor.callproc('Clay_Insert', args)
            WriteStatus = result_args[4]
            if WriteStatus == 'OK-W':
                #print(Dateofposition+" record writen to DB")
                ErrorDesc = Dateofposition+" record written to DB"
                db.commit()
            elif WriteStatus == 'DUPE':
                #print(Dateofposition+" record already in DB")
                ErrorDesc = Dateofposition+" record already in DB"
            else:
                #print(result_args[4]+" "+Dateofposition+" record FAILED")
                ErrorDesc = Dateofposition+" record write FAILED"
                WriteStatus = "FAIL"
                #endif
        except:
            WriteStatus = 'DATE'
            ErrorDesc = Dateofposition+" Invalid Date passed to S/P"
        # End except

    finally:
        # All done! Close the database connections
        cursor.close()
        db.close()
        return WriteStatus, ErrorDesc;
# END OF FUNCTION =============================================================

# Call it
Dateofposition = '2018-04-22 08:09:11.123245' #YYYY-MM-DD HH:MM:SS.123456
OpeningPosition = 662.36
EMA1 = 657.17
EMA2 = 649.61
WriteStatus = '===='
ErrorDesc = '===='

WriteStatus, ErrorDesc = Write_ClayLog( Dateofposition, OpeningPosition, EMA1, EMA2 )
print("=======================================================================")
print("WriteStatus = "+WriteStatus+" Reason:"+ErrorDesc)
print("=======================================================================")
