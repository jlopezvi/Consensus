var default_pimage = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAH0AAAB3CAYAAAAuG09DAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMDY3IDc5LjE1Nzc0NywgMjAxNS8wMy8zMC0yMzo0MDo0MiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTUgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjc1RDU4OENCN0ExMTExRTY4MDIxODRERTAxNzE1RjEwIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjc1RDU4OENDN0ExMTExRTY4MDIxODRERTAxNzE1RjEwIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6NzVENTg4Qzk3QTExMTFFNjgwMjE4NERFMDE3MTVGMTAiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6NzVENTg4Q0E3QTExMTFFNjgwMjE4NERFMDE3MTVGMTAiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7o9+opAAAcVklEQVR42uxdCZAdxXn+Zy+ttCvtSghd6EZCRiDMaQxaJ8iADRiD4+AS5kpQXBXLFCGkCsfYgJNwRiQhPrCcKgJOgFg4KRuwi9iBlGQiCYIxsREgBEJISOgGaXXtpd3J9/ebt9vT83dPv7fvmJXcqtG8fW/evOn+/rv//jsIw5B+146uVjeYL6+gmv7XIf4F+Geezc9dze8a6r/CuL4VxyQcU3DMxGfT8dkEvD42+mwUjhE4GnHwg/fh6MRxCPfch7vtxfW78L3tOG/E+xvw/mbcfSte77X1S392Us8WxF5L/Yr3gaw9Nu9jfraAwsqDLgFu+8x8cPM7+WtcHaU44ONwOhHnhbi2Da/nxQc4SCWigQEfuE6/XvutNXh/JV4+gfNanHcmnyvo7735m8m/9XFJZwDpdRpzuFowGPG+3BgoFxfo1/hyhNCm4ZrbcW7DdXN8fydtIH0G2/h8HV4yEdyJY5OvlHJJtPjvxiUBGWOWv+48JawqDLou3n0H1WeAjM9ZRN+L95ibZ8U5Sx6MQiSUjeh8CQRtfSQFbsWx3RdoXSqahOqSdDpBVA10H91to2KXqEf7FnM0jtPT9KkPMfnoZMkmcelc4XdfiSTATX6gBzHVEhqiP62PVQG91A1EVItOLUWnLsOf420cNzA4A4DUUwuO42g4TaZhNBPHNFhsE2C0HItjNI6RVAs7LsC7NXjVR734fif+P4RjP/XQHjpMu6ibdlAHbcSxnrpoC/7ejPcPpqoLo+3AZ0/js8UApjdr1nsmQAfYw3FaiuNKDNYwu9U7wIUNNJaaaC4108cA56l4fTKAnghwW3FFQwmM0x4Avgf/bwPkr9EB+g1I4yW8XqcIQxLBAhF04ViGEV68gPo6fgf6AOAP4nQtjpFpQDeC+ZvpbMB9MS4+B6/nKh6vVGNCOEhvwL9bTR/Qz0EILwPVbTFxHchEsB/Ho+D6G45q0AH2/Ii757l0WB14uJnOAtCfg5A+HwL6BFxZX/WBYwI4RG9BFvw3COApaqdVUBndaV9bg4NF/qqjCnSA3ZoX5a4gRD0dQ2PoUgjs6xR316m4SjYb2wUHIPq306O0m54GOXwQs7YpaZUvi8Dfe8SDDsAvwen7UdRMbPU0DkL8izDB/ghgnzrkQpys+xn8HfQ4wN/pMvY24/gygH/miAQdYDewVY6fWxRY/FQW4xPoj8HZf6qMsqHe2PjbRv8EAviBsv4dBt/DEdd3HzGgA3COnD2FY45p8OSBH0ufoan0NThdbXSktXa47e/RfRD4z7gCMBzhuxzArxvyoAPwC3H6GY4GySpvpOn4dzsE+jXwnBvoSG0hDLzt9BhtojupMxe1lYJFzOmXAvhnhyzoyym4Hp152BbEYL09A4PQSDPLNtCH6G3FafvpV8rVYv86xCsOzNSAyOogY5rpJEiYT8BovAjPMqOsg32I3gHkd+ApfuiaWFoE4B8ZcqAD8L9FZ74q6bFh4OvpdBd095fKpEtfp130E4D9SxwvAuCDXt9jA5LVDBuQLfR7ZQV/Gz1EG+jWmJVvjNMSAP+XQwb05bnJh/lStKoFrtfx9ADO55SBi9bSVvouuOhH4Ojd1lh/Wly7Frw/mhYoo3IMfRp/N5VJ16+i9fQXSgpZxP0qAN+WedChw1fjdI40wOPoCzSbvqM4qrSth7bA7d9M91CXcpHkCRLTgLRF/fQQMBMnc/4x9DlIqPElH/wekOg6uhGS6T9siSEvAPhzMws6OHwVHvZc88H59RRQ9PEQ6QENLzF3vwUteQuE5E9tYjL1PZ82AuQ6mW6mSXAnaRDJC3Jgh6d3bgPRPmB5Zlq9gPrml/I3a0oE+JI84LpxwsbSTPobAH5/iQEPwSP/Sr+lC/oBD428HQlcV5qT/ZfY9HsLHLmY3gU4pW61GBcenxn012L2EZ74XEjQJZni9LyVbs6J10IgckemUGntkU4M/btw87bT4165ePLUbHHz88whH4HlPY4WlkXPb6Yl6NsdsRi+ZuWXzKofbLrUBTg9ayYbMIfPAIdPoa+WdFD2wiJ/Cxx3EEZbIRkuLjBdhp7kVrGoPw1uYL3KtywP8O/Q12zPc+ECCp+rmniHyJmNh/npQELhQJsGMVhqwNkVW0tXQY+/aQVZ0uFp3BtYVECopTnGn+MtqJZlZXPneNxYQkrPz+PN414V0HMZLvQk5dKJYw84BQbPNPpGiYfiMMTeN/rnrl062sax+X9p3zG/Gwif74a13avyI8rTmGkm001S1msjnuFJHv+Kg44fXoFHmWsCMI6ugOF2d8kt3H30Cn1IP+8Xx4WIb/350kS/ngat630zTfsAnqeT3i5nzAzG3b1qPPU+RU7nXMV3lQQdevy+KM88NiAj6SxouwdVDlqp2x56tt+4CQyO1P+5AJe4OUzY/DmicqkN/oxnzQ7Sb8oateNx5PEcSWdoBNf/3G3g9vsqAjp+aDR++mpzMDjhIRd4KY9xc5BetXKz/i9MyV3VP49/jzTxn/s0THzXdOPKPyHG4zkLwPP4ChLr6uXAoxKcvhSdn2wO/EyIolH0sbJ0PITu7KANAucGVgGtc3NSxMffzwOti3/97qZnkr8unxxZ7taCceXxTRJhODnIZSCVD3RwOQdfFpJhFI2jK2kCLSpbp/sgTPsioyk+F50EV7LEJREuiW4bodh+q5faqVJtIv0JjR/ILtPtjYXLtaBYOTh9qZkA0Ag7c6YKr9aUscuBVWSnrRiRDLhQ+Ke7Zu6FEPrntVS5FtB0NQ09QxqDpWUBHVz+PZxOMQd1Bt1Rtvlw/RFrogQLCTyX6xY38Cihy03Ssvn3kvtWW+J5hLQ2Avb8DLpd8i5OAbd/r6SgA/BhbDSYXHMMXQzR/sWyd5YBb4gMGVecXI+wSVwuqwM5mOMT1eNVM5VurErH0iUJycTGNYAfVjLQcwmNam231uEWmkq3lcU9S4LJi5BarLrYzt+hCGbo4acn3bu4O5fj9KaKg87jPYVuVeNvRCxGFSLma1J88lrc7Bo9OMBtAl1VlkQIW8uDbhO7OjiS+NYNuoDIax28REj6QNfmFuRUvLXQfHD8VZIBeo1vpK4mJULFxlu97u5wEsQE+kpFO8oDbCt8IIVMQ40rpev9rfakT59/rxriPd+OoxtU2pnxjIzT0kGDjna5yQkT6BqVTFjJxjnxgVAAgQyujXMziRwfCI6d5N6Fln/V1On5xgs3OYNYINTLBwU6RMUDuOU4/cYcGRpP11W8k3VRpM/llrncLdd7gcN/jxuCgbHsqpWq2RgHXrlr2nqM22A4vS0wBmIsCKk5V9qloo3Xnkvi3SXqXfF4G3HYqkWY0oQw3JzXW83GOIyly4zxyOFWFOiglok4nRm/kJcdXU2lnkHzE0ctYqaLSQQ2TvXX30Fq+lRO8gyvmiGnP/F4tUhkmBk5PDPCrzDQ8cW7zfdG0Vlq9Wg1Wn20YlXOIUvq4jSXTJ9k0bkkIFeIduC7XNGipgouW5LbzwY7iFHYu4sR723mQHIacG2VlgvnSog0JUR8KAZhAof5JUfgzOCNrDJ0d60ZAn5M1UHn5dtjgIsh3lNFfI3gm09FJ2frFM8VIMbQBVXqWi910/uiwRYkgiihKNqlOXhTHdhcQpOYcq9rVYJmWGShn1I2xoXd6HgMgmYzjt6g40u3maJzJH1cVYCoRttIf0Vrobv0Yj8uYGwGmttts8sAift5qve3dD5tp3+pOuhNNAeq9+xEr3UcfcR7W5KaPq1WkFejHaDXwentIte59LfE9fHPZQs9cIRm8685i6cHz8RLqarfaqF6L5Kes80L9OVUw47fifp7DfBHR9H8qnVpJJ1mrTvn4ljJYo+L9vQJmDSCGhl3cKrWGB89uyZ6vhNX5PB0g44un2SKxCY6BcdHqtYhpuK8EWez2F2i2JwHt7l1enTdZQLm78Xly0bRuZkAnfHhKJ3wvCelgh5SbumGzkWc8BhUsWBAEzi9mc5IBF0k/1uwYsXAjaTvg/7qjST692Fsro3LSl8IA3dyJkBnfHI4JQh7oQ+ntyV9wVOr3KE6cPtnnIaYGbiRzDnbYkaf6VrpGo6GZamxGhSilW1O0LnUFy6cZ4Y/qxF2NVsLfTIRDPFNiLBxvyQlQovuNqUEc3hrRkR7vo2gk5X9ZfRvXlTCTQYdHZtkDlwDHQfddVwGOnS8yseTQq42EZ/U3ZTKxWSJ15vfbgZX1ZV8nf3g2jCaBCadKBHsJCvo6NgUk7obcKPaeNJMlSJPrRjoU7xi6CRC6GeN2zYjMF8300fLnAxazBi10HCaKhH1FJdOn2WKseE0u6pGXFxnnWHlQNsatUDk49CpJtKIIq8/s9YYJ17pLkQXZ7lAn6zrtZxbMiUzneKoU42FANMicS69L4VZXfdmf7iJTqcstnoDr+jZJ7tAn6QHLXJ13iZmpkPsRQynE6257jKXB4nazHJ+XGC10uMShVRRYrYvstjyeBkEPMkF+rHmgNVnyFjhma3j6R5l1EkAmrpXirzZuDdwiHT9XlxyfHq0djyLjWcjzbAy/h3rAr3VHIzaKqcEmW0MBn0afVMU2em5cHbJEIr6PX5fdtNOoEdAdHMyC3o95JAgyVpdoLeYA1OXAcs9KeZPiyVK+ljmgSMjRp9k0YM8gRH94yVFDRljgqQ0HCWHORygD0/eJHs11oep2MG0VEvbbumnG4GSxBgODg8yXr+2VsswcuGqg95oVl+oxAqW4nz2k51ASa/jEXZyfj8UCKhpCNSe1/HSRHyjKyJXQ4kBCzLZuZE035oXZ0+0oAQJ2ER+YBANu4rNQ6IGvZjfV+OKyPXpxTTNZTzZAv1MlQVq1oZJcnd6po3L+g/7XaHjhgjo4irdPpd47zQFYUgdmewaA9AUz/VwFhaSJ1fk3RvjZU3yRHYO1MqYIQB5h5QB1OkCvcMcvN6Mgs455630yVRDTMqPkySCS1KEylU8n4ZCY7yETKEOF+jtJkf0qu3EstnG0ueVrnVlz0hVKNIievHaFEE0jfqpIQL6fiETOGh3gb7X5Iwe+jCzHeRY/GiAkdyXPHByu5ktIwV59NRqLgSQhelln5bHyyDmvS7Qd5lRKN57NLt2ah1NpVtikzBBCrdLaVCuyN1wmg4+v5GGSsvjZUjsXS6Xbau5YL/TKMuZtcZ7r0ylrzt99TTSsRl3TEzH099naqYxrSXxUuOw1cXpW0xR16X2i8t2G0OXqLCsLSIX98xJ8N3jkbr8dxog2FvLvJdLqZuOl+a4bXH56etNDumid9Siomy7KV3UB202sCBRLjuS3ADTRgADRNBXxqK/pTfiumG7v53oD/qx3sXpm00O6aD30PH2jHeXS47VJ4wwWyAmcARu3EVGs+6jtwP2rVIkcrML9K26cROqnc02g9a3Zry7fVYjztBt4g4P5lVhRqOQ6fp8a/9CT6PZdXq0w+8afTBy1Y7XDKnOy5Uk7NxvWu3JSZqh0Xhv1+7IO9Pc0jXSzs3GCpdwpR6G5NcHylziuhTi3YcAbFLAvsCBhpSwP0D/J1XfWOkxYsETpgjkzeKybcx1R4ZcaA3K6MkQrgpS8WVMvSmlBrOkz7v7N/UzCPyJVNDR5ddNMce11jvozQyLtbVq6bBUfyaeCRNY348vYsy930P7oCc3DAnQeV+bfE38MLbtYA5PJ+iQ/7txWqtTPK/D3kerMuqmdKjdik0XTRLfyaXK0nr1QFuDfhD3fnRIgM5beDJORqrX2ghPL4W40hyYD+kXahOLrFntG+l2EORqa4UpqTiwbQ5dSqbaQQ/h+EHGIT9MH0T72xgzhyu9rSAMxF0mF+ynF9UWl9nQX70A+tcQ6tfBofwHUVcPqCjZiJOsd2nBYy/+571QN9F9cF13ZBJy3jJsH/2vEHMI77IauNJmfCuohhGerev3WfSPNJn+rIKi+yBE1m61bQYX9eG90LvB24cAwwG4J4c1cVYaYnLfawTNUMkUnCDJCRy85KueJqgqU0EUHKpG20LfpvX052Yf3oZotxYJshWSYRE/W9eHu+lJted5OTJkeTdkNhY7QLVsPDH1chy5m7YB/D0qXuDvkw/sueJKpZLu5brukCK8d/vvycu4eTHIMLBCE51EjXQCNYMYeNODYSCGoAKbAPTiiRgX0812iXYXp080Izk1qhDJ09RKC0r0wAdgK/wXHvrHtBeGSBeEqIsDXbsku8BK21c1bT/1+ISMe19XbrzWjaVAM81VCZxcIn1Emcq37KXlsNkvju3NGrVJ4PRtBYEeAc+O35l65ybS9RBuDw0qaME6eRf9SOlj1s2VCH/4qAGpJLhrj3XfzXm5RHcLna/2YR9NF5RwiTPbG1+CLHzEfP6XAfhZRYWzctG5uBjdDU4/MIiwbCd08lq6Fs7jVSLgvnHvtOXFaWvXbOLdVuBAIp5koEdeD98Jm2QH/Rs48iL0+wr0+1clisCtUXiYa+tDSxTOC/QFFN6MbuzUO9wD54D3LS+m7aOX0PFLob2XWStDuDlH4tr0GjEugvIpaiAFe/TnMOvcBBZXMW8XraFPgfTvVPp4MI1xYDyM59y5gPpuLhr0qD1lbkO5kx6DWfVGgYD/D6j8D9DNN2Jc4cO1+esDiufAufLyfWPsLh1vWwTpo/8Dx3UcRNlI34T/8XnliRTnpr2hcDAlFOPl8/207TwW43Y9uihjcfU+PVjAA74GwK9WU396IMQWJNGjZ2TwcyAA4xLnYYGqoxAX0Fz+5Lt5b77tgRH7Gl0GMf1ywaC/T99VHk+CnogWDxp0GAS9OD1mPvgu6Kh2j9DsYdiXbGx0wZt0VXqQkhVtxfrd4t68t9u9SwMmzWYIUr6XtjUIxx5eoy9AEr5YUMh1F/1Q+q3HIrxosOKdIurZpxswLKLeo3sU37vaZlqidLnJHWkVJEIPcFyb50k7LZs7OoXe3OyuHp1m7NnO+dedcFVfpz/EOKVzfC+u5nHPxdlj6m6fL5d7gQ7q4USxx82B/ID+k7ZrFJfU47+GGPqOyH2utWT58KnE8VJ1KUnMu7bpIiGxwnfHpmI8jaQUCRJWfhccrzeVCtzkvMdOjDeP+8A49ttHj8Pw7ioZ6BHwX8FDv2oO5Ca6CyLqHYve+XYskhamcFOy6qO9kqM5gEldbl+waDfEBkjBtkDCtae6T6Bn4BeSS6ZZ1K+nm5VSlN3dDWq84+6hYpBXAXhBe6YVEilIiA+ue75R7f/ZZ4Qs19KH8CFlp6vwiJkN0MDCOYHwnmvDH70u7MDfSRvDtrLVVW9eNi5lBbaLfgLrR9o2tQ8jfZuagzBtCdxhMRXYvEEHt68mIxODf5T97m30cOzaD+k5pXckLpEWFZqi3vyetBRJ5xxpX3Sdl1yAEyWXQ4UJAiAH14cJF1TartPmuZjG5hb6u35w820b/TN8pmXS7z8BLl9dNtCjh1+MH0wkz2+gWwDxSzG/3BbU0Et92TbhkQIvUiEhW504eX1a4Ai8+EUA7QZZcg4gbpvYiSwZwdui3Dk9qLWBvi4R4ZZCjLeiQV9AfXt0o24gUtcOfXQjzruUhXkwSq9yWbxBaqAjPbJm0+02n18qB+oy3mzLmm3KSlIDtlRrikmo+PPmjDVOW9kNTX9DIvIW3fPx83J4FNysEy6utoJqmJUTZaXH0RV0LKzQdXQNHvSA1ehxbZiTlpacdp9CvuMbpAk9Ztds79uyelz35p0VP0q/gL10j5qFFNpKAP6JYkO4xW7Mch4ejq35ufrD7qB/j5IfDloHyWaJp9VjHyAOSo3bu+q2p+3UZKsnL5mjPjs7pk3iSGqMOXsj3Q25+WPp3m/gXucNJm5fFKdH3M6ZNZyC2WgOAi/820O/TKXsUNSFSR863Q3y43DJU0iudvHfXDtNMhUjWfj1aPp9NX6CW9uJ8ykw3t4eDOhFT+5CvPAPf1aiag4r8oP7coY5W5UW/QpT/Xc7MFKQJ/4s5Az/mvo7jXN9bAz99RiM2156PmEjROfPDhbwQYEeAf8cHnVR0qvsVsAzxwcO3RVq7o5ZotMdz07Xkzawpa00peCLjzsp6+4woY5sQWST6EcrCfm8TV0tAuDPUQnaoNM4YNE/gg7ebw5EL3UB+OfREVY/DY4BTVI0WXZLTkuLckXL5OpTdq4NLAThStuSCcX03+WtB1oxTnnAhXY/GOwRKlErWqcLOp6n3c6VBoM5nmPxfUaCYynSmHytZOl+he7HlhZF1BMyTfcusHJdE42iM/pFutC/1QC8pBvjlQz0CHiODp0jfTaKPq4Wzed9zkIGt1BA/N0jPepuS7qkWPDF1zCT5hVIC+Rw4yTKRpqt1hWYzxLd4wWI9JLvEFRS0LktV+m3wfxA4IpmtTdcjUqs8PFvbXPg9pm3wDv12cV9hRKbr9egN95dKYDs421FLdesAoe3URlayXefAWXiQcMlkjHEaT48jdhKn3BySJqvbY92yeFS2fqmoiRI0qh0z+5JBRC4/z0YBx4PS5xiSbkALwuna6L+epwetnEUi3vOqOHDFTsPDW1pC3Omid+0+LyvfVFIDr256IIXRvDRTi+4CHtRKY22ioIeAX8hTj9Dpxsk0dxIkzAIM6O04O6i9fhg7QLfad3iv8vbA5ylpqJZ0lnUWTfeuxSAP0tlbmUFPQKe9794Cp2aY9PJozAgPFFzgF713jXJRzX42ArFxuFdQR7d+GuieVQL8mbCdsTwOS32cgC+jirQyg56ZNw1oHNLyQjkhDFLtkltpNtB7wP+dzxCt/YNd2R3yn/iJs369yGcEbDKG2iCKhbAtWAcUUFORlgMW6hi5T4qArrG9Zfg9H0cU2wDx4sCeWvoHtoZm6L1AdAnSOMrOVxE57IleN0aFx7kZ+c+OIhwM/7+Mrj7GapwqyjoEfC8ke9SdPhK13W8KrQJbg2XAemA9OvVCvmlrTfz5U6fSJsptgPRBWpQGxHXAHK2yDkWkWIPcBrMYqny0xEJ+oDIr2FfnkX+PBeAPKC8FJj3ZePieJ20ObZKs5BZrdCS4eIrAczascNpGohzMghyr1pmzYmgOmEIS6a5ZBtnu6hFA+dRHx1VoEe6nv/xcplriTdQcETNgmgndd6Mj9fIdyndv0lJAJdONoM2Lv/ZtixZJ0AuSsDim/MGpAijhcP34/1H8d4N+ptHJegrBmJDvIJ/KQbmSgzMMB/9mgthTlbbbHBiUTcGnytX9BjLfaR15T62AQPcQBPVXmf1NFZtz3UY9+blBsLCQRvhsU5aFmWsdphq5qgF3Rj4WsqJ/MtwjPdxu+KVIcaqXSN5G68a/N8Xrb7jKlR9aqsLPh9Wddf4p/hbPOFRB9VRqypJ1+HvWqU+eqldLctilcKpX/bkiwFBroWed+Dvp4Nc4mKvTQoMSdBXCFFcW1aKb0679vpbOLXh79Pl0iIkztW7dm0yRbsU/fPJjHXE8l/hdf14eZP0DD4Gpd2WSNawLJZo6kpORULHbH6zaUwZHb8p+nsCzvcyAeCqWfH89uQ69bSYvRwf9wdFuD+X1l6Jd2/FeXtabqAtj84nCFSqiGXJOb3YUKj7+/2w8n6bvKSGJyPmFBMn9826TZFSHDljjr4TxybXdl9pUiRMqAbyztFbUGQZ00GD7iPOfd/3KfqjuUHj8DdvzrYwIoJ5abFyd9o0ieVQos/XRCA/wZUY8d5OSgEpjRBckslUXbZrixXv/y/AAOPCrTzrL6iXAAAAAElFTkSuQmCC';
$('.cropme_profile').simpleCropper();
function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i=0; i<ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1);
    if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
  }
  return "";
 var name = cname + "=";
 var ca = document.cookie.split(';');
 for(var i=0; i<ca.length; i++) {
   var c = ca[i];
   while (c.charAt(0)==' ') c = c.substring(1);
   if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
 }
 return "";
};
var hostEmail = '';
var guestEmail = '';
$(document).ready( function() {
  $(document).on('change', ':file', function() {
    var input = $(this),
      numFiles = input.get(0).files ? input.get(0).files.length : 1,
      label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
  });

  function isValidEmailAddress(emailAddress) {
    var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
    return pattern.test(emailAddress);
  };

  $('.emailValidate').focusout(function(){
    var email = $(this).val();
    var parent = $(this).parent().parent();
    var cond = false;
    if(parent.hasClass('home--login'))
      cond = true;
    if( !isValidEmailAddress( email ) ) {
      $(this).addClass('errorInput');
      if(cond)
        $('.login--button').prop('disabled', true);
      else
        $('.register--button').prop('disabled', true);
    } else {
      $(this).removeClass('errorInput');
      if(cond)
        $('.login--button').prop('disabled', false);
      else
        $('.register--button').prop('disabled', false);
    }
  });

  $('#fullname_r').keypress(function(e){
    var r = /^[a-zA-ZäöüÄÖÜáéíóúÁÉÚÍÓÑñ\b ]+$/;
    var verified = r.test(String.fromCharCode(e.which));
    if (!verified)
      e.preventDefault();
  });

  $('#position_r').keypress(function(e){
    var r = /^[a-zA-ZäöüÄÖÜáéíóúÁÉÚÍÓÑñ\b ]+$/;
    var verified = r.test(String.fromCharCode(e.which));
    if (!verified)
      e.preventDefault();
  });

  $(document).ready( function() {
    $(':file').on('fileselect', function(event, numFiles, label) {
      var input = $(this).parents('.input-group').find(':text'),
        log = numFiles > 1 ? numFiles + ' files selected' : label;

      if( input.length ) {
        input.val(log);
      } else {
        if( log ) alert(log);
      }
    });
  });

  $(document).on('click', '.login--button', function(){
    $('.login--message').hide();
    var data = {
      'email': $('#email').val(),
      'password': $('#password').val()
    };
    if(data.email == '' || data.password == ''){
      $('.login--message').empty().append('All fields must be fills!').show();
    } else {
        $.ajax({
          url: url[0] + "//" + url[2] + '/login',
          type: 'POST',
          data: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          },
          dataType: 'json',
          success: function (json) {
            if(json.result == 'Wrong: Bad password'){
              $('.login--message').empty().append('Email or Password wrong!').show();
            } else if(json.result == 'Wrong: Bad e-mail'){
              $('.login--message').empty().append('e-mail not found / not verified').show();
            } else if(json.result == 'OK'){
              //GETTING ALL IDEAS FOR NEWSFEED TO VALIDATE THE REDIRECT
              $.ajax({
                url: url[0] + "//" + url[2] + '/ideas_for_newsfeed',
                type: 'GET',
                data: JSON.stringify(data),
                headers: {
                  'Content-Type': 'application/json'
                },
                dataType: 'json',
                success: function (json) {
                  //console.log(json.data);
                  if(json.data.length > 0)
                    window.location = '/newsfeed';
                  else
                    window.location = '/home';
                }
              });
              
            }
          },
          error: function(response){
            console.log(response);
          }
        });
    }
  });

  $(document).on('click', '.register--button', function(e){
    $('.register--message').hide();
    var data = {
      'fullname': $('#fullname_r').val(),
      'email': $('#email_r').val(),
      'username': $('#username_r').val(),
      'position': $('#position_r').val(),
      'group': 'IT', //$('#group_r').val(),
      'password': $('#password_r').val(),
      'image_url': '', //$('#password').val(),
      'ifpublicprofile': $('#public_r').val(),
      'host_email': null,
      'ifemailverified': false
    };
    if(data.email == '' || data.password == '' || $('#password2_r').val() == '' || data.fullname == '' || data.username == '' || data.position == '' || data.group == ''){
        $('.register--message').removeClass('alert-success').addClass('alert-danger');
        $('.register--message').empty().append('All fields must be fills!').show();
    } else {
        if($('#password_r').val() == $('#password2_r').val()){
            $.ajax({
              url: url[0] + "//" + url[2] + '/if_participant_exists_by_email/'+data.email,
              type: 'GET',
              headers: {
                'Content-Type': 'application/json'
              },
              dataType: 'json',
              success: function (json) {
                if(json.result){
                  $('.register--message').removeClass('alert-success').addClass('alert-danger');
                  $('.register--message').empty().append('Email already taken').show();
                } else {
                  $('#modal_sign').modal('show');
                }
              },
              error: function(response){
                console.log('error');
              }
            });

        } else {
            $('.register--message').removeClass('alert-success').addClass('alert-danger');
            $('.register--message').empty().append('Passwords must be the same!').show();
        }
    }
  });

  $(document).on('click', '.register--modal', function(){
    $('.register--button').prop('disabled', 'true');
    if ($('#public_r').is(":checked"))
        opt = true;
    else
        opt = false;
    
    var newData = {
      'fullname': $('#fullname_r').val(),
      'email': $('#email_r').val(),
      'username': $('#username_r').val(),
      'position': $('#position_r').val(),
      'group': $('#group_r').val(),
      'password': $('#password_r').val(),
      'ifpublicprofile': opt,
      'ifregistrationfromemail': false,
      'host_email': 'none'
    };

    hostEmail = $('#hostEmail').val();
    if(hostEmail != null){
      newData['host_email'] = hostEmail;
      newData['ifemailverified'] = true;
      newData['ifregistrationfromemail'] = true;
    }
    
    //newData['profilepic'] = default_pimage;
    newData['profilepic'] = null;
    if($('.cropme_profile img').length){
      newData['profilepic'] = $('.cropme_profile img').attr('src');
    }
    console.log(newData);
    var redirect = false;
    $.ajax({
      url: url[0] + "//" + url[2] + '/get_ideas_created_by_participant/'+hostEmail,
      type: 'GET',
      success: function(data){
        if(data.ideas_indices.length > 0){
          redirect = true;
        }
      }
    });

    $.ajax({
      url: url[0] + "//" + url[2] + '/registration',
      type: 'POST',
      data: JSON.stringify(newData),
      headers: {
          'Content-Type': 'application/json'
      },
      dataType: 'json',
      success: function (json) {
        if(json.result != 'OK'){
          $('.register--message').removeClass('alert-danger').addClass('alert-success');
          $('.register--message').empty().append('Participant registered previously, resend email verification.').show();
          $('.register--button').prop('disabled', 'false');
        } else {
          if((json.ifhost) && (json.ifemailverified)){
            if(redirect)
              window.location = '/newsfeed';
            else
              window.location = '/home';
          }
          else{
            $('.register--message').removeClass('alert-danger').addClass('alert-success');
            $('.register--message').empty().append('E-mail verification sent.<br>Close this window and check your e-mail within the next few minutes.').show();
            $('.register--button').prop('disabled', 'false');
          }
        }
      },
      error: function(response){
        console.log(response);
      }
    });

  });

  function archive(evt) {
	var files = evt.target.files;
	for (var i = 0, f; f = files[i]; i++) {
	if (!f.type.match('image.*')) {
	  continue;
	}
	var reader = new FileReader();
	reader.onload = (function(theFile) {
	return function(e) {
	  //$('.user--icon--login').css('background-image', 'url("'+e.target.result+'")');
	  $('.user--icon--login').attr('src', e.target.result);
	};
	})(f);
      reader.readAsDataURL(f);
    }
  }
  //document.getElementById('profile_photo').addEventListener('change', archive, false);
  
  /**************************** CROPPIE FUNCTIONS ****************************/
  
  

});

var url = window.location.href;
url = url.split("/");

$( window ).load(function(){
  /*********** READY WHEN INVITATION **************/
  hostEmail = $('#hostEmail').val();
  guestEmail = $('#guestEmail').val();
  emailVerificated = $('#emailVerificated').val();
  if(emailVerificated != null){
    $('#email').val(emailVerificated);
  }
  if(hostEmail != null){
    $('#email_r').val(guestEmail).prop('disabled', true);
    $.ajax({
      url: url[0] + "//" + url[2] + '/get_fullname_for_participant_unrestricted/'+hostEmail,
      type: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      dataType: 'json',
      success: function (json) {
        //console.log(json);
        $('.home--content--left h1').html(json.fullname + ' Welcomes You!')
      },
      error: function(response){
        //console.log(response.responseText);
        //$('.login--message2').append('You have been invited by <strong>'+ response.responseText +'</strong>');
      }
    });
  }
});

