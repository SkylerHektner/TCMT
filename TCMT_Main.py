import sys
from PyQt4 import QtGui, QtCore, uic
from random import randint
import json
from datetime import datetime

class baseWidget(QtGui.QWidget):
    def __init__(self):
        super(baseWidget, self).__init__()

    def updateWholePage(self): # Just a function to be defined over later. Here for compatibility
        pass

    def clearWidget(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
        return

class charPage(baseWidget):
    def __init__(self, charDict, master):
        super(charPage, self).__init__()
        self.charDict = charDict
        self.master = master

        self.initUI()
        self.initBindings()
        self.updateWholePage()

    def updateWholePage(self):
        # Character Information
        self.nameLabel.setText(self.charDict['Name'])
        self.raceLabel.setText(self.charDict['Race'])
        self.classLabel.setText(self.charDict['Class'])
        self.alignmentLabel.setText(self.charDict['Alignment'])
        self.heightLabel.setText(self.charDict['Height'])
        self.levelLabel.setText(str(self.charDict['Level']))
        self.sexLabel.setText(self.charDict['Sex'])
        self.weightLabel.setText(self.charDict['Weight'])

        # Combat
        self.HPLabel.setText(str(self.charDict['HPMax']))
        self.ACLabel.setText(str(self.charDict['ACBase']))
        self.InitiativeLabel.setText(str(self.charDict['Initiative']))

        # Stats
        self.updateStats()

        # XP
        self.XPLabel.setText(str(self.charDict['Current XP']))

        # Proficiency Bonus
        self.proficiencyLabel.setText(str(self.charDict['Proficiency Bonus']))

        # Languages
        self.updateLanguages()

    def updateStats(self):
        order = ((self.STRLabel, self.STRAbilityLabel, self.STRSavingLabel, 'STR', self.STRCheckBox),
                 (self.DEXLabel, self.DEXAbilityLabel, self.DEXSavingLabel, 'DEX', self.DEXCheckBox),
                 (self.CONLabel, self.CONAbilityLabel, self.CONSavingLabel, 'CON', self.CONCheckBox),
                 (self.INTLabel, self.INTAbilityLabel, self.INTSavingLabel, 'INT', self.INTCheckBox),
                 (self.CHALabel, self.CHAAbilityLabel, self.CHASavingLabel, 'CHA', self.CHACheckBox),
                 (self.WISLabel, self.WISAbilityLabel, self.WISSavingLabel, 'WIS', self.WISCheckBox))

        for g in order:
            g[0].setText(str(self.charDict[g[3]][0]))
            num = self.charDict[g[3]][0]
            at = (num-10)//2
            if at > 0: at = '+' + str(at)
            else: at = str(at)
            st = (num-10)//2
            if self.charDict[g[3]][1]: st += self.charDict['Proficiency Bonus']
            if st > 0: st = '+' + str(st)
            else: st = str(st)
            g[1].setText(at)
            g[2].setText(st)
            if self.charDict[g[3]][1] and not g[4].isChecked(): g[4].toggle()

    def updateLanguages(self):
        self.langList.clear()
        for l in self.charDict['Languages']:
            self.langList.addItem(l)

    def initUI(self):
        uic.loadUi('UI/CharInfo.ui', self)
        self.show()

    def initBindings(self):
        # Stats
        self.STRAddButton.clicked.connect(lambda : self.statChanger(self.STRLabel, 'add', ['STR',0],
                                                                   self.STRAbilityLabel, self.STRSavingLabel))
        self.DEXAddButton.clicked.connect(lambda : self.statChanger(self.DEXLabel, 'add', ['DEX',0],
                                                                   self.DEXAbilityLabel, self.DEXSavingLabel))
        self.CONAddButton.clicked.connect(lambda : self.statChanger(self.CONLabel, 'add', ['CON',0],
                                                                   self.CONAbilityLabel, self.CONSavingLabel))
        self.INTAddButton.clicked.connect(lambda : self.statChanger(self.INTLabel, 'add', ['INT',0],
                                                                   self.INTAbilityLabel, self.INTSavingLabel))
        self.WISAddButton.clicked.connect(lambda : self.statChanger(self.WISLabel, 'add', ['WIS',0],
                                                                   self.WISAbilityLabel, self.WISSavingLabel))
        self.CHAAddButton.clicked.connect(lambda : self.statChanger(self.CHALabel, 'add', ['CHA',0],
                                                                   self.CHAAbilityLabel, self.CHASavingLabel))
        self.STRSubtractButton.clicked.connect(lambda : self.statChanger(self.STRLabel, 'sub', ['STR',0],
                                                                   self.STRAbilityLabel, self.STRSavingLabel))
        self.DEXSubtractButton.clicked.connect(lambda : self.statChanger(self.DEXLabel, 'sub', ['DEX',0],
                                                                   self.DEXAbilityLabel, self.DEXSavingLabel))
        self.CONSubtractButton.clicked.connect(lambda : self.statChanger(self.CONLabel, 'sub', ['CON',0],
                                                                   self.CONAbilityLabel, self.CONSavingLabel))
        self.INTSubtractButton.clicked.connect(lambda : self.statChanger(self.INTLabel, 'sub', ['INT',0],
                                                                   self.INTAbilityLabel, self.INTSavingLabel))
        self.WISSubtractButton.clicked.connect(lambda : self.statChanger(self.WISLabel, 'sub', ['WIS',0],
                                                                   self.WISAbilityLabel, self.WISSavingLabel))
        self.CHASubtractButton.clicked.connect(lambda : self.statChanger(self.CHALabel, 'sub', ['CHA',0],
                                                                   self.CHAAbilityLabel, self.CHASavingLabel))
        self.STRCheckBox.stateChanged.connect(self.changeProfSTR)
        self.DEXCheckBox.stateChanged.connect(self.changeProfDEX)
        self.CONCheckBox.stateChanged.connect(self.changeProfCON)
        self.INTCheckBox.stateChanged.connect(self.changeProfINT)
        self.CHACheckBox.stateChanged.connect(self.changeProfCHA)
        self.WISCheckBox.stateChanged.connect(self.changeProfWIS)


        # Combat
        self.HPAddButton.clicked.connect(lambda : self.valChanger(self.HPLabel, 'add',['HPMax']))
        self.HPSubtractButton.clicked.connect(lambda : self.valChanger(self.HPLabel, 'sub',['HPMax']))

        self.ACAddButton.clicked.connect(lambda : self.valChanger(self.ACLabel, 'add',['ACBase']))
        self.ACSubtractButton.clicked.connect(lambda : self.valChanger(self.ACLabel, 'sub',['ACBase']))

        self.InitiativeAddButton.clicked.connect(lambda : self.valChanger(self.InitiativeLabel, 'add',['Initiative']))
        self.InitiativeSubtractButton.clicked.connect(lambda : self.valChanger(self.InitiativeLabel, 'sub',['Initiative']))

        # Proficiency Bonus
        self.proficiencyAddButton.clicked.connect(lambda : self.profChanger(self.proficiencyLabel,
                                                                           'add', ['Proficiency Bonus']))
        self.proficiencySubtractButton.clicked.connect(lambda : self.profChanger(self.proficiencyLabel,
                                                                                'sub',['Proficiency Bonus']))

        # Character Information
        self.nameEditButton.clicked.connect(lambda : self.getInfo('Enter Name:',
                                                                   'Name', self.nameLabel, 'text'))
        self.levelEditButton.clicked.connect(lambda : self.getInfo('Enter Level: ',
                                                                   'Level', self.levelLabel, 'int'))
        self.raceEditButton.clicked.connect(lambda : self.getInfo('Enter Race:',
                                                                  'Race', self.raceLabel, 'text'))
        self.classEditButton.clicked.connect(lambda : self.getInfo('Enter Class:',
                                                                   'Class',self.classLabel, 'text'))
        self.alignmentEditButton.clicked.connect(lambda : self.getInfo('Enter Alignment:',
                                                                       'Alignment', self.alignmentLabel, 'text'))
        self.heightEditButton.clicked.connect(lambda : self.getInfo('Enter Height: ',
                                                                    'Height', self.heightLabel, 'text'))
        self.sexEditButton.clicked.connect(lambda : self.getInfo('Enter Sex',
                                                                 'Sex', self.sexLabel, 'text'))
        self.weightEditButton.clicked.connect(lambda : self.getInfo('Enter Weight:',
                                                                    'Weight', self.weightLabel, 'text'))
        self.backgroundButton.clicked.connect(self.showBackground)

        # Languages
        self.langAddButton.clicked.connect(self.addLang)
        self.langRemoveButton.clicked.connect(self.removeLang)

        # XP
        self.XPAddButton.clicked.connect(lambda : self.changeXP('add'))
        self.XPSubtractButton.clicked.connect(lambda : self.changeXP('subtract'))
        self.XPZeroButton.clicked.connect(self.zeroXP)


    def changeProfSTR(self, state):
        self.charDict['STR'][1] = state
        self.updateStats()
    def changeProfDEX(self, state):
        self.charDict['DEX'][1] = state
        self.updateStats()
    def changeProfCON(self, state):
        self.charDict['CON'][1] = state
        self.updateStats()
    def changeProfINT(self, state):
        self.charDict['INT'][1] = state
        self.updateStats()
    def changeProfWIS(self, state):
        self.charDict['WIS'][1] = state
        self.updateStats()
    def changeProfCHA(self, state):
        self.charDict['CHA'][1] = state
        self.updateStats()


    def zeroXP(self):
        self.charDict['Current XP'] = 0
        self.XPLabel.setText('0')

    def changeXP(self, action):
        num, ok = QtGui.QInputDialog.getInt(self, 'Change XP', 'Input Value to ' + action)
        if ok:
            if action == 'add': self.charDict['Current XP'] += num
            else: self.charDict['Current XP'] -= num
            self.XPLabel.setText(str(self.charDict['Current XP']))

    def addLang(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Language', 'Enter Language Name')
        if ok:
            self.charDict['Languages'].append(text)
            self.updateLanguages()

    def removeLang(self):
        l = self.langList.currentItem().text()
        if l in self.charDict['Languages']:
            i = self.charDict['Languages'].index(l)
            del self.charDict['Languages'][i]
            self.updateLanguages()

    def getInfo(self, message, pointer, label, type):
        if type == 'text':
            text, ok = QtGui.QInputDialog.getText(self, pointer, message)
            if ok:
                label.setText(text)
                self.charDict[pointer] = text

        elif type == 'int':
            num, ok = QtGui.QInputDialog.getInt(self, pointer, message)
            if ok:
                label.setText(str(num))
                self.charDict[pointer] = num

    def showBackground(self):
        self.d = d = QtGui.QDialog()
        d.setWindowModality(QtCore.Qt.ApplicationModal)
        d.setWindowTitle('Background')
        d.resize(500,400)

        entry = QtGui.QTextEdit(d)
        entry.setPlainText(self.charDict['Background'])

        b1 = QtGui.QPushButton('Save', d)
        b2 = QtGui.QPushButton('Cancel', d)
        b1.clicked.connect(lambda : self.saveBackground(entry, d))
        b2.clicked.connect(d.reject)

        grid = QtGui.QGridLayout(d)
        grid.addWidget(entry, 0, 0, 1, 2)
        grid.addWidget(b1, 1, 0)
        grid.addWidget(b2, 1, 1)

        d.exec_()

    def saveBackground(self, entry, d):
        self.charDict['Background'] = entry.toPlainText()
        d.accept()

    def statChanger(self, label, action, pointer, Alabel, Slabel):
        self.valChanger(label, action, pointer)
        num = self.charDict[pointer[0]][pointer[1]]
        at = str((num-10)//2)
        if int(at) > 0: at = '+' + at
        st = (num-10)//2
        if self.charDict[pointer[0]][1]: st += self.charDict['Proficiency Bonus']
        if st > 0: st = '+' + str(st)
        else: st = str(st)

        Alabel.setText(at)
        Slabel.setText(st)

    def profChanger(self, label, action, pointer):
        self.valChanger(label, action, pointer)
        self.updateStats()

    def valChanger(self, label, action, pointer):
        if len(pointer) == 1:
            if action == 'add':
                self.charDict[pointer[0]] += 1
            else:
                self.charDict[pointer[0]] -= 1
            t = str(self.charDict[pointer[0]])
            label.setText(t)
        else:
            if action == 'add':
                self.charDict[pointer[0]][pointer[1]] += 1
            else:
                self.charDict[pointer[0]][pointer[1]] -= 1
            t = str(self.charDict[pointer[0]][pointer[1]])
            label.setText(t)


class invPage(baseWidget):
    def __init__(self, charDict, master):
        super(invPage, self).__init__()
        self.charDict = charDict
        self.master = master

        self.initUI()
        self.initBindings()

    def initUI(self):
        uic.loadUi('UI/Inventory.ui', self)
        self.infoManager = QtGui.QGridLayout(self.infoBox)

        # Money Section
        self.moneyManager = QtGui.QGridLayout(self.moneyBox)

        order = ('Resources/Platinum.gif','Resources/Gold.gif','Resources/Silver.gif','Resources/Bronze.gif')
        for x,s in enumerate(order):
            x *= 2
            x += 1
            l = QtGui.QLabel(self.moneyBox)
            pix = QtGui.QPixmap(s)
            l.setPixmap(pix)
            self.moneyManager.addWidget(l, 0, x)

        font = QtGui.QFont('Consolas', 12, QtGui.QFont.Bold)
        self.moneyLabels = [QtGui.QLabel(),QtGui.QLabel(),QtGui.QLabel(),QtGui.QLabel()]
        for x,l in enumerate(self.moneyLabels):
            l.setAlignment(QtCore.Qt.AlignRight)
            l.setText('0')
            l.setFont(font)
            self.moneyManager.addWidget(l, 0, x*2)



    def initBindings(self):
        # Display Item Information
        self.inventoryList.clicked.connect(self.displayItemInfo)

        # Update Inventory Listing when changing sorting
        self.nameSortButton.clicked.connect(self.updateInventory)
        self.quantSortButton.clicked.connect(self.updateInventory)
        self.typeSortButton.clicked.connect(self.updateInventory)
        self.equipSortButton.clicked.connect(self.updateInventory)

        #New Item
        self.newItemButton.clicked.connect(self.newItemDio)

        #Delete Item
        self.removeButton.clicked.connect(self.deleteItem)

        #Edit Item
        self.editButton.clicked.connect(self.editItem)

        #Equip Item
        self.equipButton.clicked.connect(self.equipItem)

        #Change Money
        self.addMoneyButton.clicked.connect(self.addMoney)
        self.subMoneyButton.clicked.connect(self.subMoney)

    def addMoney(self):
        self.d = d = QtGui.QDialog()
        uic.loadUi('UI/Add_Money.ui', d)
        d.accepted.connect(lambda : self.changeMoney('add'))
        d.exec_()

    def subMoney(self):
        self.d = d = QtGui.QDialog()
        uic.loadUi('UI/Remove_Money.ui', d)
        d.accepted.connect(lambda: self.changeMoney('sub'))
        d.exec_()

    def changeMoney(self, action):
        if action == 'add':
            self.charDict['Money'][0] += self.d.bronzeBox.value()
            self.charDict['Money'][1] += self.d.silverBox.value()
            self.charDict['Money'][2] += self.d.goldBox.value()
            self.charDict['Money'][3] += self.d.platinumBox.value()
        elif action == 'sub':
            self.charDict['Money'][0] -= self.d.bronzeBox.value()
            self.charDict['Money'][1] -= self.d.silverBox.value()
            self.charDict['Money'][2] -= self.d.goldBox.value()
            self.charDict['Money'][3] -= self.d.platinumBox.value()
        self.updateMoney()

    def updateMoney(self):
        l = self.charDict['Money']
        while l[0] > 9 or l[1] > 9 or l[2] > 9:
            for x in range(3):
                if l[x] > 9:
                    l[x] -= 10
                    l[x + 1] += 1
                    break

        while l[0] < 0 or l[1] < 0 or l[2] < 0:
            for x in range(3):
                if l[x] < 0:
                    l[x] += 10
                    l[x + 1] -= 1
                    break

        self.charDict['Money'] = l

        for x,label in enumerate(self.moneyLabels):
            x += 1
            label.setText(str(l[-x]))


    def editItem(self):
        text = self.inventoryList.currentItem().text(1)
        for x, item in enumerate(self.charDict['Items']):
            if item['Name'] == text:
                break

        self.d = d = QtGui.QDialog()

        if item['Type'] == 'Misc':
            uic.loadUi('UI/New_Misc_Item.ui', d)
        elif item['Type'] == 'Weapon':
            uic.loadUi('UI/New_Weapon.ui', d)
            # Fill in Weapon Specific Data
            d.damageEdit.setText(item['Damage'])
            d.propertiesEdit.setText(item['Properties'])
            d.rangeEdit.setText(item['Range'])
        elif item['Type'] == 'Armour':
            uic.loadUi('UI/New_Armour.ui', d)
            # Fill in Armour Specific Data
            d.classComboBox.insertItem(0,item['Class'])
            d.ACEdit.setText(item['AC Bonus'])

        #Fill in Misc Item Data
        d.nameEdit.setText(item['Name'])
        d.quantityBox.setValue(item['Quantity'])
        w,u = item['Weight'].split(' ')
        d.weightBox.setValue(int(w))
        if u == 'Kg.': d.kilogramButton.setChecked(True)
        elif u == 'St.': d.stoneButton.setChecked(True)
        d.descriptionText.setHtml(item['Description'])

        d.accepted.connect(lambda : self.editItemFinal(item))

        d.exec_()

    def editItemFinal(self, item):
        i = self.charDict['Items'].index(item)
        del self.charDict['Items'][i]
        if item['Type'] == 'Misc': self.newMisc()
        elif item['Type'] == 'Weapon': self.newWeapon()
        elif item['Type'] == 'Armour': self.newArmour()
        self.clearWidget(self.infoManager)


    def equipItem(self):
        text = self.inventoryList.currentItem().text(1)
        for x, item in enumerate(self.charDict['Items']):
            if item['Name'] == text:
                break
        curStatus = self.charDict['Items'][x]['Equipped']
        newStatus = not curStatus
        self.charDict['Items'][x]['Equipped'] = newStatus

        self.updateInventory()
        self.clearWidget(self.infoManager)


    def deleteItem(self):
        text = self.inventoryList.currentItem().text(1)
        for x,item in enumerate(self.charDict['Items']):
            if item['Name'] == text:
                break
        del self.charDict['Items'][x]
        self.updateInventory()
        self.clearWidget(self.infoManager)

    def newItemDio(self):
        self.d = d = QtGui.QDialog()
        uic.loadUi('UI/New_Item.ui', d)

        d.buttonBox.accepted.connect(self.newItem)

        d.exec_()

    def newItem(self):
        t = self.d.choiceList.currentItem().text()

        self.d = d = QtGui.QDialog()
        if t == 'Misc':
            uic.loadUi('UI/New_Misc_Item.ui', d)
            d.accepted.connect(self.newMisc)
        elif t == 'Weapon':
            uic.loadUi('UI/New_Weapon.ui', d)
            d.accepted.connect(self.newWeapon)
        elif t == 'Armour':
            uic.loadUi('UI/New_Armour.ui', d)
            d.accepted.connect(self.newArmour)

        d.exec_()

    def newMisc(self):
        name = self.d.nameEdit.text()
        if name == '':
            return
        quantity = self.d.quantityBox.value()
        weight = str(self.d.weightBox.value())
        if self.d.poundButton.isChecked(): weight += ' Lb.'
        elif self.d.kilogramButton.isChecked(): weight += ' Kg.'
        elif self.d.stoneButton.isChecked(): weight += ' St.'
        description = self.d.descriptionText.toPlainText()
        type = 'Misc'

        self.charDict['Items'].append(
            {'Type':type, 'Quantity':quantity, 'Name':name, 'Weight':weight, 'Description':description, 'Equipped':False})

        self.updateInventory()

    def newWeapon(self):
        name = self.d.nameEdit.text()
        if name == '':
            return
        quantity = self.d.quantityBox.value()
        weight = str(self.d.weightBox.value())
        if self.d.poundButton.isChecked():
            weight += ' Lb.'
        elif self.d.kilogramButton.isChecked():
            weight += ' Kg.'
        elif self.d.stoneButton.isChecked():
            weight += ' St.'
        description = self.d.descriptionText.toPlainText()
        type = 'Weapon'
        damage = self.d.damageEdit.text()
        properties = self.d.propertiesEdit.text()
        range = self.d.rangeEdit.text()

        self.charDict['Items'].append(
            {'Type': type, 'Quantity': quantity, 'Name': name, 'Weight': weight, 'Description': description,
             'Damage':damage,'Properties':properties,'Range':range, 'Equipped':False})

        self.updateInventory()

    def newArmour(self):
        name = self.d.nameEdit.text()
        if name == '':
            return
        quantity = self.d.quantityBox.value()
        weight = str(self.d.weightBox.value())
        if self.d.poundButton.isChecked(): weight += ' Lb.'
        elif self.d.kilogramButton.isChecked(): weight += ' Kg.'
        elif self.d.stoneButton.isChecked(): weight += ' St.'
        description = self.d.descriptionText.toPlainText()
        type = 'Armour'
        Class = self.d.classComboBox.currentText()
        AC = self.d.ACEdit.text()

        self.charDict['Items'].append(
            {'Type':type, 'Quantity':quantity, 'Name':name, 'Weight':weight, 'Description':description,
             'Class':Class,'AC Bonus':AC, 'Equipped':False})

        self.updateInventory()

    def updateWholePage(self):
        self.updateInventory()
        self.clearWidget(self.infoManager)
        self.updateMoney()

    def updateInventory(self):
        self.inventoryList.clear()
        order = ['Quantity','Name','Equipped','Type','Weight', 'Description']

        items = self.charDict['Items']

        if self.nameSortButton.isChecked():
            items = sorted(items, key=lambda k: k['Name'].lower())
        elif self.quantSortButton.isChecked():
            items = sorted(items, key=lambda k: k['Quantity'], reverse=True)
        elif self.typeSortButton.isChecked():
            items = sorted(items, key=lambda k: k['Type'])
        elif self.equipSortButton.isChecked():
            items = sorted(items, key=lambda k: k['Equipped'], reverse=True)

        for item in items:
            l = []
            for o in order:
                if o == 'Weight' and item[o][0] == '0': l.append('')
                else: l.append(str(item[o]))
            i = QtGui.QTreeWidgetItem(self.inventoryList, l)

    def displayItemInfo(self):
        text = self.inventoryList.currentItem().text(1)
        for item in self.charDict['Items']:
            if item['Name'] == text:
                break

        self.clearWidget(self.infoManager)
        if item['Type'] == 'Misc':
            order = ['Name','Type','Equipped','Quantity','Description','Weight']
        elif item['Type'] == 'Weapon':
            order = ['Name', 'Type','Equipped','Damage', 'Properties', 'Range', 'Quantity', 'Description', 'Weight']
        elif item['Type'] == 'Armour':
            order = ['Name', 'Type','Equipped', 'Class', 'AC Bonus', 'Quantity', 'Description', 'Weight']
        for x,key in enumerate(order):
            l = QtGui.QLabel('<b>'+key+'</b>', self.infoBox)
            self.infoManager.addWidget(l, x, 0)
            l = QtGui.QLabel(str(item[key]), self.infoBox)
            l.setWordWrap(True)
            self.infoManager.addWidget(l, x, 1)

class rollerPage(baseWidget):
    def __init__(self, charDict, master):
        super(rollerPage, self).__init__()
        self.charDict = charDict
        self.master = master

        self.initUI()
        self.initBindings()

    def updateWholePage(self):
        for i in reversed(range(self.macroGrid.count())):
            self.macroGrid.itemAt(i).widget().setParent(None)
        r=0
        c=0
        for macro in self.charDict['Macros']:
            b = self.makeMacroButton(macro)
            self.macroGrid.addWidget(b, r, c)
            c += 1
            if c > 4:
                c=0
                r+=1
        self.clearResBox()

    def initUI(self):
        uic.loadUi('UI/Roller.ui', self)
        self.macroWidget = QtGui.QWidget(self.macroGroup)
        self.macroGrid = QtGui.QGridLayout(self.macroWidget)
        self.macroScrollArea.setWidget(self.macroWidget)
        self.macroGrid.setContentsMargins(2,2,2,2)
        self.macroGrid.setHorizontalSpacing(2)
        self.macroGrid.setVerticalSpacing(2)

    def initBindings(self):
        # Default Dice
        self.d4Button.clicked.connect(lambda : self.roller(['d4']))
        self.d6Button.clicked.connect(lambda : self.roller(['d6']))
        self.d8Button.clicked.connect(lambda : self.roller(['d8']))
        self.d10Button.clicked.connect(lambda : self.roller(['d10']))
        self.d12Button.clicked.connect(lambda : self.roller(['d12']))
        self.d20Button.clicked.connect(lambda : self.roller(['d20']))

        # Buttons
        self.clearButton.clicked.connect(self.clearResBox)
        self.editButton.clicked.connect(self.editMacroDio)

    def editMacroDio(self):
        self.d = d = QtGui.QDialog()
        uic.loadUi('UI/Edit_Macros.ui', d)
        d.setWindowTitle('Edit Macros')

        # Update List
        for macro in self.charDict['Macros']:
            d.macroList.addItem(macro[0])

        # Bindings
        d.addButton.clicked.connect(self.newMacroDio)
        d.removeButton.clicked.connect(self.removeMacro)
        d.editMacroButton.clicked.connect(self.reviseMacroDio)
        d.exitButton.clicked.connect(d.reject)
        d.exec_()

    def reviseMacroDio(self):
        name = self.d.macroList.currentItem().text()
        for macro in self.charDict['Macros']:
            if name == macro[0]:
                break

        self.d.accept()
        self.d.close()
        self.d2 = d2 = QtGui.QDialog(self)
        uic.loadUi('UI/New_Macro.ui', self.d2)
        d2.setWindowTitle('Edit Macro')

        d2.macroBinding.addItem('None')
        for skill in self.charDict['Skills']:
            d2.macroBinding.addItem(skill[0])

        d2.macroNameEntry.setText(name)
        dice = []
        for s in macro[1]:
            if s[0] == 'd': dice.append(s)
            elif s[0] == 'n': d2.flatAdd.setValue(int(s[1:]))
            elif s[0] == 's':
                d2.macroBinding.insertItem(0, s[1:])
                d2.macroBinding.setCurrentIndex(0)

        d={}
        for die in dice:
            try:
                d[die] += 1
            except:
                d[die] = 1
        sides = (self.d2.d1number, self.d2.d2number, self.d2.d3number, self.d2.d4number)
        number = (self.d2.d1amount, self.d2.d2amount, self.d2.d3amount, self.d2.d4amount)
        for x, items in enumerate(d.items()):
            die, num = items
            sides[x].setValue(int(die[1:]))
            number[x].setValue(int(num))

        # bindings
        d2.newMacroCancelButton.clicked.connect(d2.reject)
        d2.newMacroSaveButton.clicked.connect(lambda: self.reviseMacroSave(macro))

        d2.exec_()

    def reviseMacroSave(self, oldMacro):
        i = self.charDict['Macros'].index(oldMacro)
        del self.charDict['Macros'][i]
        self.saveMacro()


    def removeMacro(self):
        m = self.d.macroList.currentItem().text()
        for macro in self.charDict['Macros']:
            if m == macro[0]:
                i = self.charDict['Macros'].index(macro)
                del self.charDict['Macros'][i]
                break
        self.d.macroList.clear()
        for macro in self.charDict['Macros']:
            self.d.macroList.addItem(macro[0])
        self.updateWholePage()

    def newMacroDio(self):
        self.d.accept()
        self.d.close()
        self.d2 = d2 = QtGui.QDialog()
        uic.loadUi('UI/New_Macro.ui', self.d2)
        d2.setWindowTitle('New Macro')

        d2.macroBinding.addItem('None')
        for skill in self.charDict['Skills']:
            d2.macroBinding.addItem(skill[0])

        # Bindings
        d2.newMacroCancelButton.clicked.connect(d2.reject)
        d2.newMacroSaveButton.clicked.connect(self.saveMacro)

        d2.exec_()

    def saveMacro(self):
        name = self.d2.macroNameEntry.text()
        macro = []
        sides = (self.d2.d1number, self.d2.d2number, self.d2.d3number, self.d2.d4number)
        number = (self.d2.d1amount, self.d2.d2amount, self.d2.d3amount, self.d2.d4amount)
        for side,number in zip(sides,number): # add dice
            s = side.text()
            n = number.text()
            if s == '0': continue
            s = 'd' + str(s)
            for x in range(int(n)):
                macro.append(s)
        f = self.d2.flatAdd.text() # add any flat addition
        if f == '0': pass
        else:
            f = 'n' + str(f)
            macro.append(f)
        b = self.d2.macroBinding.currentText()
        if b == 'None': pass
        else:
            b = 's' + b
            macro.append(b)
        self.charDict['Macros'].append([name,macro])
        self.updateWholePage()
        self.d2.accept()

    def makeMacroButton(self, macro):
        b = QtGui.QPushButton(macro[0])
        b.clicked.connect(lambda : self.roller(macro[1]))
        b.setMinimumSize(0, 100)
        return b

    def clearResBox(self):
        self.resultLabel.clear()

    def roller(self, macro):
        self.clearResBox()
        tot = 0
        if len(macro) == 1: charList = [0]
        else: charList = [0] * (len(macro)*2 +1)
        for x, s in enumerate(macro): # Creates Number Labels from dice data
            c = ''
            if s[0] == 'd': # d denotes dice
                r = randint(1, int(s[1:]))
                tot += r
                c = ' ' + str(r) + ' '
                if r == int(s[1:]):
                    c = '<font color=green>' + c + '</font>'
                elif r == 1:
                    c = '<font color=red>' + c + '</font>'
            elif s[0] == 'n': # n denotes fixed addition
                c = s[1:]
                c = '<font color=grey> ' + c + ' </font>'
                tot += int(s[1:])
            elif s[0] == 's': # s denotes skill
                for item in self.charDict['Skills']:
                    if item[0] == s[1:]:
                        break
                    else:
                        item = 'ERROR'
                if item != 'ERROR':
                    c = item[4]
                    c = '<font color=purple> ' + str(c) + ' </font>'
                    tot += item[4]
                else:
                    c = 'Broken Binding'
                    c = '<font color=red> ' + c + ' </font>'

            charList[x*2] = c
        self.master.statusBar().showMessage('Rolled!', 1500)


        for x in range(len(macro)-1): # Insert plus signs
            col = x*2 + 1
            charList[col] = '+'
        if len(macro) > 1: # Insert = sign and total amount
            col = len(macro)*2 - 1
            charList[col] = '='
            col = len(macro)*2
            charList[col] = str(tot)

        # Grid them accordingly
        t = ''
        for c in charList:
            t += c
        self.resultLabel.setText(t)


class skillPage(baseWidget):
    def __init__(self, charDict, master):
        super(skillPage, self).__init__()
        self.charDict = charDict
        self.master = master

        self.initUI()
        self.initBindings()

    def updateWholePage(self):
        self.updateSkillLists()
        self.clearInfoSection()

    def updateSkillLists(self):
        self.learnedSkills.clear()
        self.unLearnedSkills.clear()

        for item in self.charDict['Skills']:
            # Ensure modifier accuracy
            i = self.charDict['Skills'].index(item)
            if item[2]:
                self.charDict['Skills'][i][4] = self.charDict['Proficiency Bonus'] + item[3] + \
                                                (self.charDict[item[1]][0]-10)//2
            else:
                self.charDict['Skills'][i][4] = item[3] + (self.charDict[item[1]][0]-10)//2

            # Add item to list
            name = item[0]
            mod = item[4]
            if mod >= 0: mod = '+' + str(mod)
            else: mod = str(mod)
            s = name + ' (' + mod + ')'
            if item[2]: self.learnedSkills.addItem(s)
            else: self.unLearnedSkills.addItem(s)

    def clearInfoSection(self):
        self.nameLabel.setText('Name: ')
        self.learnedLabel.setText('Learned: ')
        self.attributeLabel.setText('Attribute: ')
        self.modifierLabel.setText('')
        self.descriptionLabel.setText('')
        self.totalBonusLabel.setText('')
        try: self.modSubButton.clicked.disconnect()
        except: pass
        try: self.modAddButton.clicked.disconnect()
        except: pass

    def initUI(self):
        uic.loadUi('UI/Skills.ui', self)

    def initBindings(self):
        self.newButton.clicked.connect(self.newSkillDio)
        self.learnedSkills.clicked.connect(self.changeButton_UnLearn)
        self.unLearnedSkills.clicked.connect(self.changeButton_Learn)
        self.unLearnedSkills.clicked.connect(self.displayUnLearnedInfo)
        self.learnedSkills.clicked.connect(self.displayLearnedInfo)
        self.learnedSkills.clicked.connect(self.swapDeleteLearned)
        self.unLearnedSkills.clicked.connect(self.swapDeleteUnLearned)

    def swapDeleteLearned(self):
        try: self.deleteButton.clicked.disconnect()
        except: pass
        self.deleteButton.clicked.connect(lambda: self.delete(self.learnedSkills))

    def swapDeleteUnLearned(self):
        try: self.deleteButton.clicked.disconnect()
        except: pass
        self.deleteButton.clicked.connect(lambda: self.delete(self.unLearnedSkills))

    def delete(self, menu):
        t = menu.currentItem().text()
        t = t[0:t.index('(')-1]
        for item in self.charDict['Skills']:
            if t == item[0]:
                i = self.charDict['Skills'].index(item)
                del self.charDict['Skills'][i]
                self.updateWholePage()

    def displayUnLearnedInfo(self):
        t = self.unLearnedSkills.currentItem().text()
        t = t[0:t.index('(')-1]
        for item in self.charDict['Skills']:
            if item[0] == t: break
        self.nameLabel.setText('Name: ' + item[0])
        self.learnedLabel.setText('Learned: ' + str(item[2]))
        mod = (self.charDict[item[1]][0]-10)//2
        if mod >= 0: mod = '(+' + str(mod) + ')'
        else: mod = '(' + str(mod) + ')'
        self.attributeLabel.setText('Attribute: ' + item[1] + mod)
        self.modifierLabel.setText(str(item[3]))
        self.descriptionLabel.setText(item[5])
        self.totalBonusLabel.setText(str(item[4]))
        try: self.modSubButton.clicked.disconnect()
        except: pass
        try: self.modAddButton.clicked.disconnect()
        except: pass
        self.modSubButton.clicked.connect(lambda: self.modifySkillBonus('sub', item))
        self.modAddButton.clicked.connect(lambda: self.modifySkillBonus('add', item))

    def displayLearnedInfo(self):
        t = self.learnedSkills.currentItem().text()
        t = t[0:t.index('(')-1]
        for item in self.charDict['Skills']:
            if item[0] == t: break
        self.nameLabel.setText('Name: ' + item[0])
        mod = self.charDict['Proficiency Bonus']
        if mod >= 0: mod = '(+' + str(mod) + ')'
        else: mod = '(' + str(mod) + ')'
        self.learnedLabel.setText('Learned: ' + str(item[2]) + mod)
        mod = (self.charDict[item[1]][0]-10)//2
        if mod >= 0: mod = '(+' + str(mod) + ')'
        else: mod = '(' + str(mod) + ')'
        self.attributeLabel.setText('Attribute: ' + item[1] + mod)
        self.modifierLabel.setText(str(item[3]))
        self.descriptionLabel.setText(item[5])
        self.totalBonusLabel.setText(str(item[4]))
        try: self.modSubButton.clicked.disconnect()
        except: pass
        try: self.modAddButton.clicked.disconnect()
        except: pass
        self.modSubButton.clicked.connect(lambda: self.modifySkillBonus('sub', item))
        self.modAddButton.clicked.connect(lambda: self.modifySkillBonus('add', item))


    def modifySkillBonus(self, op, skill):
        for item in self.charDict['Skills']:
            if item == skill:
                i = self.charDict['Skills'].index(skill)
                break
        if op == 'sub': self.charDict['Skills'][i][3] -= 1
        else: self.charDict['Skills'][i][3] += 1
        self.updateSkillLists()
        self.modifierLabel.setText(str(self.charDict['Skills'][i][3]))
        self.totalBonusLabel.setText(str(self.charDict['Skills'][i][4]))


    def newSkillDio(self):
        self.d = d = QtGui.QDialog()
        uic.loadUi('UI/NewSkill.ui',d)
        d.cancelButton.clicked.connect(d.reject)
        d.saveButton.clicked.connect(self.saveNewSkill)
        d.exec_()

    def saveNewSkill(self):
        name = self.d.nameLineEdit.text()
        description = self.d.descriptText.toPlainText()
        attribute = self.d.attributeBox.currentText()
        if name != '':
            self.charDict['Skills'].append([name, attribute, False, 0, 0, description])
            self.updateSkillLists()
            self.d.accept()

    def changeButton_UnLearn(self):
        try: self.learnButton.clicked.disconnect()
        except: pass
        self.learnButton.setText('Un-Learn')
        self.learnButton.clicked.connect(self.unlearn)

    def changeButton_Learn(self):
        try: self.learnButton.clicked.disconnect()
        except: pass
        self.learnButton.setText('Learn')
        self.learnButton.clicked.connect(self.learn)

    def unlearn(self):
        t = self.learnedSkills.currentItem().text()
        t = t[0:t.index('(')-1]
        for item in self.charDict['Skills']:
            if t == item[0]:
                i = self.charDict['Skills'].index(item)
                self.charDict['Skills'][i][2] = False
                self.updateSkillLists()
                self.clearInfoSection()

    def learn(self):
        t = self.unLearnedSkills.currentItem().text()
        t = t[0:t.index('(')-1]
        for item in self.charDict['Skills']:
            if t == item[0]:
                i = self.charDict['Skills'].index(item)
                self.charDict['Skills'][i][2] = True
                self.updateSkillLists()
                self.clearInfoSection()

class spellPage(baseWidget):
    def __init__(self,charDict, master):
        super(spellPage, self).__init__()
        self.charDict = charDict
        self.master = master

        self.initUI()
        self.initBindings()

    def initUI(self):
        uic.loadUi('UI/Spell.ui', self)
        self.infoManager = QtGui.QGridLayout(self.spellInfoBox)

    def initBindings(self):
        # Spell Modifier Adjustement
        self.incSpellModifierButton.clicked.connect(self.incSpellModifier)
        self.subSpellModifierButton.clicked.connect(self.subSpellModifier)

        # Spell Info Display
        self.spellList.clicked.connect(self.showSpellInfo)

        # Sorting
        self.nameSortButton.clicked.connect(self.updateSpellInventory)
        self.levelSortButton.clicked.connect(self.updateSpellInventory)

        # Add Spell
        self.newSpellButton.clicked.connect(self.newSpell)
        # Edit Spell
        self.editSpellButton.clicked.connect(self.editSpell)
        # Delete Spell
        self.deleteSpellButton.clicked.connect(self.deleteSpell)
        # Add Spell To Daily List
        self.addToDailyButton.clicked.connect(self.addToDaily)

        # Clear Daily Spells
        self.clearDailyButton.clicked.connect(self.clearDaily)
        # Use Daily Spell
        self.useDailyButton.clicked.connect(self.useDaily)
        # UnUse Daily Spell
        self.unUseDailyButton.clicked.connect(self.unUseDaily)

        # Add New Daily Preset
        self.newSpellPresetButton.clicked.connect(self.newDailySpellPreset)
        # Delete Daily Preset
        self.deleteSpellPresetButton.clicked.connect(self.deleteSpellPreset)
        # Load Daily Preset
        self.loadSpellPresetButton.clicked.connect(self.loadDailySpellPreset)

    def updateWholePage(self):
        self.updateSpellModifier()
        self.updateSpellInventory()
        self.updateSpellPresets()

    def loadDailySpellPreset(self):
        text = self.spellPresetList.currentItem().text()
        for item in self.charDict['Daily Spell Presets']:
            if item['Name'] == text:
                break

        self.clearDaily()
        for spellName in item['Spells']:
            w = QtGui.QTreeWidgetItem(self.dailySpellList, [spellName, 'Not Used'])
            self.dailySpellList.addTopLevelItem(w)

    def updateSpellPresets(self):
        self.spellPresetList.clear()
        for item in self.charDict['Daily Spell Presets']:
            self.spellPresetList.addItem(item['Name'])

    def deleteSpellPreset(self):
        text = self.spellPresetList.currentItem().text()
        for item in self.charDict['Daily Spell Presets']:
            if item['Name'] == text:
                break
        i = self.charDict['Daily Spell Presets'].index(item)
        del self.charDict['Daily Spell Presets'][i]
        self.updateSpellPresets()

    def newDailySpellPreset(self):
        numSpells = self.dailySpellList.topLevelItemCount()
        if numSpells == 0: return
        l = []
        for x in range(numSpells):
            text = self.dailySpellList.topLevelItem(x).text(0)
            l.append(text)

        input = QtGui.QInputDialog.getText(self, 'Name of Daily Spell Preset', 'Enter the name of your new preset: ')
        if not input[1]: return
        name = input[0]
        d = {'Name':name, 'Spells':l}
        self.charDict['Daily Spell Presets'].append(d)

        self.updateSpellPresets()

    def unUseDaily(self):
        self.dailySpellList.currentItem().setText(1, 'Not Used')
        f = QtGui.QFont()
        f.setBold(False)
        self.dailySpellList.currentItem().setFont(1, f)

    def useDaily(self):
        self.dailySpellList.currentItem().setText(1,'Used')
        f = QtGui.QFont()
        f.setBold(True)
        self.dailySpellList.currentItem().setFont(1,f)

    def clearDaily(self):
        self.dailySpellList.clear()

    def addToDaily(self):
        text = self.spellList.currentItem().text(0)
        new = QtGui.QTreeWidgetItem(self.dailySpellList, [text,'Not Used'])
        self.dailySpellList.addTopLevelItem(new)

    def deleteSpell(self):
        text = self.spellList.currentItem().text(0)
        for spell in self.charDict['Spells']:
            if spell['Name'] == text:
                break
        i = self.charDict['Spells'].index(spell)
        del self.charDict['Spells'][i]
        self.updateSpellInventory()
        self.clearWidget(self.infoManager)

    def editSpell(self):
        text = self.spellList.currentItem().text(0)
        for spell in self.charDict['Spells']:
            if spell['Name'] == text:
                break

        self.d = d = QtGui.QDialog()
        uic.loadUi('UI/New_Spell.ui', d)
        d.setWindowTitle('Edit Spell')

        d.nameEdit.setText(spell['Name'])
        d.levelBox.setValue(spell['Level'])
        d.castingEdit.setText(spell['Casting Time'])
        d.componentsEdit.setText(spell['Components'])
        d.durationEdit.setText(spell['Duration'])
        d.rangeEdit.setText(spell['Range'])
        d.descriptionText.setHtml(spell['Description'])

        d.accepted.connect(lambda: self.editSpellFinal(spell))
        d.exec_()

    def editSpellFinal(self, spell):
        i = self.charDict['Spells'].index(spell)
        del self.charDict['Spells'][i]
        self.newSpellFinal()

    def newSpell(self):
        self.d = d = QtGui.QDialog()
        uic.loadUi('UI/New_Spell.ui', d)
        d.accepted.connect(self.newSpellFinal)

        d.exec_()

    def newSpellFinal(self):
        if self.d.nameEdit.text() == '': return
        name = self.d.nameEdit.text()
        level = self.d.levelBox.value()
        cast = self.d.castingEdit.text()
        components = self.d.componentsEdit.text()
        duration = self.d.durationEdit.text()
        range = self.d.rangeEdit.text()
        description = self.d.descriptionText.toPlainText()

        spell = {'Name':name, 'Level':level, 'Casting Time':cast, 'Components':components, 'Duration':duration,
                 'Range':range, 'Description':description}
        self.charDict['Spells'].append(spell)
        self.updateSpellInventory()
        self.clearWidget(self.infoManager)


    def showSpellInfo(self):
        self.clearWidget(self.infoManager)

        text = self.spellList.currentItem().text(0)
        for spell in self.charDict['Spells']:
            if spell['Name'] == text:
                break

        order = ('Name', 'Level', 'Casting Time', 'Range', 'Components', 'Duration')
        for x,s in enumerate(order):
            l = QtGui.QLabel('<b>' + s + '</b>', self.spellInfoBox)
            self.infoManager.addWidget(l, x, 0)
            l = QtGui.QLabel(str(spell[s]), self.spellInfoBox)
            l.setWordWrap(True)
            self.infoManager.addWidget(l, x, 1)

        b = QtGui.QGroupBox('Description', self.spellInfoBox)
        self.infoManager.addWidget(b, x+1, 0, 1, 2)
        m = QtGui.QGridLayout(b)
        l = QtGui.QLabel(spell['Description'], b)
        l.setWordWrap(True)
        m.addWidget(l, 0, 0)


    def updateSpellInventory(self):
        self.spellList.clear()

        spells = self.charDict['Spells']

        if self.nameSortButton.isChecked():
            spells = sorted(spells, key=lambda k: k['Name'].lower())
        elif self.levelSortButton.isChecked():
            spells = sorted(spells, key=lambda k: k['Level'])

        for spell in spells:
            w = QtGui.QTreeWidgetItem(self.spellList, [spell['Name'], str(spell['Level'])])
            self.spellList.addTopLevelItem(w)

    def incSpellModifier(self):
        self.charDict['Spell Modifier'] += 1
        self.updateSpellModifier()

    def subSpellModifier(self):
        self.charDict['Spell Modifier'] -= 1
        self.updateSpellModifier()

    def updateSpellModifier(self):
        self.spellModifier.setText(str(self.charDict['Spell Modifier']))

class FPage(baseWidget):
    def __init__(self,charDict, master):
        super(FPage, self).__init__()
        self.charDict = charDict
        self.master = master

        self.initUI()
        self.initBindings()

    def initUI(self):
        uic.loadUi('UI/Feats.ui', self)
        self.featBoxManager = QtGui.QGridLayout(self.featDescriptionBox)

    def initBindings(self):
        self.newFeatButton.clicked.connect(self.newFeat)
        self.deleteFeatButton.clicked.connect(self.deleteFeat)
        self.featList.clicked.connect(self.displayFeatDescription)
        self.editFeatButton.clicked.connect(self.editFeat)

    def editFeat(self):
        self.d = d = QtGui.QDialog()
        uic.loadUi('UI/New_Feat.ui', d)
        d.setWindowTitle('Edit Feat')

        text = self.featList.currentItem().text()
        for feat in self.charDict['Feats']:
            if feat['Name'] == text:
                break

        self.d.nameEdit.setText(feat['Name'])
        self.d.descriptionText.setHtml(feat['Description'])

        self.d.accepted.connect(lambda: self.editFeatFinal(feat))

        self.d.exec_()

    def editFeatFinal(self, feat):
        i = self.charDict['Feats'].index(feat)
        del self.charDict['Feats'][i]
        self.newFeatFinal()

    def displayFeatDescription(self):
        self.clearWidget(self.featBoxManager)
        text = self.featList.currentItem().text()
        for feat in self.charDict['Feats']:
            if feat['Name'] == text:
                break
        l = QtGui.QLabel(feat['Description'], self.featList)
        l.setWordWrap(True)
        self.featBoxManager.addWidget(l)

    def newFeat(self):
        self.d = d = QtGui.QDialog()
        uic.loadUi('UI/New_Feat.ui', d)
        d.accepted.connect(self.newFeatFinal)
        d.exec_()

    def newFeatFinal(self):
        name = self.d.nameEdit.text()
        description = self.d.descriptionText.toHtml()
        self.charDict['Feats'].append({'Name':name,'Description':description})
        self.updateFeatList()
        self.clearWidget(self.featBoxManager)

    def deleteFeat(self):
        text = self.featList.currentItem().text()
        for feat in self.charDict['Feats']:
            if text == feat['Name']:
                break
        i = self.charDict['Feats'].index(feat)
        del self.charDict['Feats'][i]
        self.updateFeatList()
        self.clearWidget(self.featBoxManager)

    def updateWholePage(self):
        self.updateFeatList()
        self.clearWidget(self.featBoxManager)

    def updateFeatList(self):
        self.featList.clear()
        for feat in self.charDict['Feats']:
            self.featList.addItem(feat['Name'])


class ANPage(baseWidget):
    def __init__(self,charDict, master):
        super(ANPage, self).__init__()
        self.charDict = charDict
        self.master = master
        self.currentEntry = None

        self.initUI()
        self.initBindings()

    def initUI(self):
        uic.loadUi('UI/Adventure_Notebook.ui', self)

    def initBindings(self):
        self.newEntryButton.clicked.connect(self.newEntry)
        self.deleteEntryButton.clicked.connect(self.deleteEntry)
        self.entryList.clicked.connect(self.loadEntry)
        self.entryText.textChanged.connect(self.updateEntryText)
        self.editEntryNameButton.clicked.connect(self.editEntryName)

    def updateWholePage(self):
        self.updateEntryList()
        self.currentEntry = None
        self.entryText.clear()
        self.entryNameLabel.setText('No Current Entry (It is not saving what you are writing now)')

    def editEntryName(self):
        name, ok = QtGui.QInputDialog.getText(self, 'New Entry Name', 'Please Enter New Entry Name: ')
        if ok:
            text = self.entryList.currentItem().text(0)
            for entry in self.charDict['Adventure Entries']:
                if entry['Name'] == text:
                    break
            i = self.charDict['Adventure Entries'].index(entry)
            self.charDict['Adventure Entries'][i]['Name'] = name
            self.updateEntryList()

    def updateEntryList(self):
        self.entryList.clear()
        for item in self.charDict['Adventure Entries']:
            w = QtGui.QTreeWidgetItem(self.entryList, [item['Name'], item['Date Entered']])
            self.entryList.addTopLevelItem(w)

    def updateEntryText(self):
        if self.currentEntry == None: return
        text = self.entryText.toHtml()
        self.charDict['Adventure Entries'][self.currentEntry]['Text'] = text

    def loadEntry(self):
        text = self.entryList.currentItem().text(0)
        for item in self.charDict['Adventure Entries']:
            if item['Name'] == text:
                break
        self.currentEntry = self.charDict['Adventure Entries'].index(item)
        self.entryText.setHtml(item['Text'])
        self.entryNameLabel.setText(item['Name'])

    def deleteEntry(self):
        text = self.entryList.currentItem().text(0)
        for item in self.charDict['Adventure Entries']:
            if item['Name'] == text:
                break
        i = self.charDict['Adventure Entries'].index(item)
        del self.charDict['Adventure Entries'][i]
        self.updateEntryList()
        self.currentEntry = None
        self.entryText.clear()
        self.entryNameLabel.setText('No Current Entry (It is not saving what you are writing now)')

    def newEntry(self):
        name, ok = QtGui.QInputDialog.getText(self, 'Enter Name', 'Please Enter Entry Name: ')
        if ok:
            date = datetime.now()
            date = str(date.month)+'/'+str(date.day)+'/'+str(date.year)
            self.charDict['Adventure Entries'].append(
                    {'Name':name, 'Text':'', 'Date Entered':date}
            )
            self.entryNameLabel.setText(name)
            self.updateEntryList()
            self.currentEntry = len(self.charDict['Adventure Entries']) - 1
            self.entryText.clear()

class TCMT(QtGui.QMainWindow):
    
    def __init__(self):
        super(TCMT, self).__init__()

        self.initCharDict()
        self.initUI()
        self.initBindings()

    def initUI(self):
        uic.loadUi('UI\Main.ui', self)
        self.charP = charPage(self.charDict, self)
        self.invP = invPage(self.charDict, self)
        self.rollP = rollerPage(self.charDict, self)
        self.skillP = skillPage(self.charDict, self)
        self.FP = FPage(self.charDict, self)
        self.spellP = spellPage(self.charDict, self)
        self.ANP = ANPage(self.charDict, self)

        self.pagesGrid.addWidget(self.charP, 0, 0)
        self.pagesGrid.addWidget(self.invP, 0, 0)
        self.pagesGrid.addWidget(self.rollP, 0, 0)
        self.pagesGrid.addWidget(self.skillP, 0, 0)
        self.pagesGrid.addWidget(self.FP, 0, 0)
        self.pagesGrid.addWidget(self.spellP, 0, 0)
        self.pagesGrid.addWidget(self.ANP, 0, 0)

        self.pageSwap(self.charP)

        self.refreshStatPresetActions()

        self.show()

    def initBindings(self):
        self.charButton.clicked.connect(lambda: self.pageSwap(self.charP))
        self.FButton.clicked.connect(lambda: self.pageSwap(self.FP))
        self.invButton.clicked.connect(lambda: self.pageSwap(self.invP))
        self.rollButton.clicked.connect(lambda: self.pageSwap(self.rollP))
        self.skillButton.clicked.connect(lambda: self.pageSwap(self.skillP))
        self.spellButton.clicked.connect(lambda: self.pageSwap(self.spellP))
        self.ANButton.clicked.connect(lambda: self.pageSwap(self.ANP))

        self.actionFont.triggered.connect(self.changeAppFont)
        self.actionQuit.triggered.connect(self.close)
        self.actionSave_As.triggered.connect(self.saveAs)
        self.actionSave.triggered.connect(self.save)
        self.actionLoad.triggered.connect(self.load)
        self.actionNew_Stat_Preset.triggered.connect(self.newStatPreset)
        self.actionRemove_Stat_Preset.triggered.connect(self.removeStatPreset)

        self.actionClean_Looks.triggered.connect(lambda : self.changeStyle('cleanlooks'))
        self.actionPlastique.triggered.connect(lambda: self.changeStyle('plastique'))
        self.actionDefault.triggered.connect(lambda: self.changeStyle(self.charDict['Default Style']))

    def changeStyle(self, style):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(style))
        self.charDict['Pref Style'] = style

    def removeStatPreset(self):
        d = QtGui.QDialog()
        uic.loadUi('UI/Remove_Stat_Preset.ui', d)
        for key in self.charDict['Stat Presets']:
            if key != 'Main Stat Preset':
                d.statPresetListWidget.addItem(key)

        d.accepted.connect(lambda: self.removeStatPresetFinal(d))
        d.exec_()

    def removeStatPresetFinal(self, d):
        text = d.statPresetListWidget.currentItem().text()
        print(text)
        del self.charDict['Stat Presets'][text]
        self.charDict['Current Stat Preset'] = 'Main Stat Preset'
        self.loadCurrentStatPreset()
        self.charP.updateWholePage()
        self.refreshStatPresetActions()

    def refreshStatPresetActions(self):
        self.menuStat_Presets.clear()
        self.statPresetActions = []
        for key in self.charDict['Stat Presets']:
            action = QtGui.QAction(key, self)
            action.setCheckable(True)
            action.triggered.connect(lambda k=key, j=key: self.loadStatPreset(j,key))
            self.menuStat_Presets.addAction(action)
            self.statPresetActions.append(action)

        self.menuStat_Presets.addAction(self.actionNew_Stat_Preset)
        self.menuStat_Presets.addAction(self.actionRemove_Stat_Preset)
        for item in self.statPresetActions:
            if item.text() == self.charDict['Current Stat Preset']:
                item.setChecked(True)

    def saveCurrentStatPreset(self):
        saveDict = {'STR': self.charDict['STR'],
                    'INT': self.charDict['INT'],
                    'WIS': self.charDict['WIS'],
                    'CHA': self.charDict['CHA'],
                    'CON': self.charDict['CON'],
                    'DEX': self.charDict['DEX'],
                    'ACBase': self.charDict['ACBase'],
                    'HPMax': self.charDict['HPMax'],}
        self.charDict['Stat Presets'][self.charDict['Current Stat Preset']] = saveDict

    def loadCurrentStatPreset(self):
        instruction = ['STR','DEX','INT','WIS','CHA','CON','HPMax','ACBase']
        loadDict = self.charDict['Stat Presets'][self.charDict['Current Stat Preset']]
        for s in instruction:
            self.charDict[s] = loadDict[s]

    def loadStatPreset(self, preset, junk):
        self.saveCurrentStatPreset()
        self.charDict['Current Stat Preset'] = preset
        self.loadCurrentStatPreset()
        self.charP.updateWholePage()
        self.refreshStatPresetActions()

    def newStatPreset(self):
        text, ok = QtGui.QInputDialog.getText(self, 'New Preset Name', 'Enter name of New Stat Preset:')
        if ok:
            # Save the current stat preset
            self.saveCurrentStatPreset()

            # Switch Current Stat Preset
            self.charDict['Current Stat Preset'] = text

            # Create new Stat Preset in CharDict
            self.charDict['Stat Presets'][text] = {
                'STR': [0, False],
                'DEX': [0, False],
                'INT': [0, False],
                'WIS': [0, False],
                'CHA': [0, False],
                'CON': [0, False],
                'HPMax': 0,
                'ACBase': 0
            }

            # Load New (Now current) stat preset
            self.loadCurrentStatPreset()

            # Update Character Page
            self.charP.updateWholePage()

            # Update Stat Preset Action
            self.refreshStatPresetActions()

    def closeEvent(self, event):
        self.saveCurrentStatPreset()

        if self.charDict['Save Directory'] == '':
            quit_msg = 'Unsaved changes have been made. Do you still wish to exit?'
            reply = QtGui.QMessageBox.question(self, 'Message',
                                               quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
            return

        save = open(self.charDict['Save Directory'])
        data = json.load(save)
        if data != self.charDict:
            quit_msg = 'Unsaved changes have been made. Do you still wish to exit?'
            reply = QtGui.QMessageBox.question(self, 'Message',
                                               quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
            return

    def load(self):
        fileDirectory = QtGui.QFileDialog.getOpenFileName(self, 'Select Character to load', '/home', '*.char')
        if fileDirectory == '': return
        file = open(fileDirectory, 'r')
        data = json.load(file)
        for key in data:
            self.charDict[key] = data[key]
        self.charP.updateWholePage()
        self.invP.updateWholePage()
        self.rollP.updateWholePage()
        self.skillP.updateWholePage()
        self.FP.updateWholePage()
        self.spellP.updateWholePage()
        self.ANP.updateWholePage()
        # Check for preferred font
        if self.charDict['Font'] != '':
            font = QtGui.QFont(self.charDict['Font'])
            QtGui.QApplication.setFont(font)
        # Check for preferred style
        if self.charDict['Pref Style'] != '':
            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(self.charDict['Pref Style']))
        # Make sure to include the new stat preset actions
        self.refreshStatPresetActions()



    def saveAs(self):
        self.saveCurrentStatPreset()
        fileDirectory = QtGui.QFileDialog.getSaveFileName(self, 'Save Character As...', self.charDict['Name'], '*.char')
        if fileDirectory == '': return
        self.charDict['Save Directory'] = fileDirectory
        file = open(fileDirectory, 'w')
        json.dump(self.charDict, file)
        file.close()
        self.statusBar().showMessage('Saved!', 3000)

    def save(self):
        self.saveCurrentStatPreset()
        if self.charDict['Save Directory'] == '':
            self.saveAs()
            return
        fileDirectory = self.charDict['Save Directory']
        file = open(fileDirectory, 'w')
        file.truncate()
        json.dump(self.charDict, file)
        file.close()
        self.statusBar().showMessage('Saved!', 3000)

    def changeAppFont(self):
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            QtGui.QApplication.setFont(font)
            self.charDict['Font'] = font.toString()

    def pageSwap(self, item):
        pages = (self.charP, self.invP, self.rollP, self.skillP, self.FP, self.spellP, self.ANP)
        for page in pages:
            if item == page:
                page.show()
                page.updateWholePage()
            else:
                page.hide()


    def initCharDict(self):
        self.charDict = {
        # INFORMATION
        'Name':'None',
        'Race':'None',
        'Level':0,
        'Class':'None',
        'Background':'None',
        'Languages':['Common'],
        'Alignment':'None',
        'Sex':'None',
        'Height':'None',
        'Weight':'None',
        'XP':0,
        'Proficiency Bonus':0,
        'Spell Modifier':0,
        'Save Directory':'',
        'Font':'',
        'Default Style':self.style().objectName(),
        'Pref Style':'',

        # BASE STATS
        'STR':[0,False],
        'DEX':[0,False],
        'CON':[0,False],
        'INT':[0,False],
        'WIS':[0,False],
        'CHA':[0,False],

        #Stat Presets
        'Current Stat Preset':'Main Stat Preset',
        'Stat Presets':{'Main Stat Preset':
                            {'STR':[0,False],'DEX':[0,False],'CON':[0,False],'INT':[0,False],'WIS':[0,False],'CHA':[0,False],
                             'HPMax':0, 'ACBase':0}},

        # MISC
        'HPMax':0,
        'HPCurrent':0,
        'ACBase':0,
        'Initiative':0,
        'Current XP':0,

        # EQUIPS
        'LHand': None,
        'RHand': None,
        'Boots': None,
        'Chest': None,
        'Helm': None,
        'Gloves': None,
        'Ring1': None,
        'Ring2': None,
        'Ring3': None,
        'Ring4': None,
        'Amulet1': None,
        'Amulet2': None,
        'Cape': None,

        # The Rest
        'Feats':[],
        'Spells':[],
        'Daily Spell Presets':[],
        'Proficiencies':[],
        'Abilities':[],
        'Items':[],
        'Skills':[
        ['Acrobatics', 'DEX', False, 0, 0,
         'Covers your attempt to stay on your feet in a tricky situation, such as when you’re trying to run across a sheet of ice, balance on a tightrope, or stay upright on a rocking ship’s deck.'],
        ['Animal Handling','WIS', False, 0, 0,
         'When there is any question whether you can calm down a domesticated animal, keep a mount from getting spooked, or intuit an animal’s intentions. Also for performing risky mounting actions or risky maneuvers on your mount.'],
        ['Arcana', 'INT', False, 0, 0,
         'Measures your ability to recall lore about spells, magic items, eldritch symbols, magical traditions, the planes of existence, and the inhabitants of those planes.'],
        ['Athletics', 'STR', False, 0, 0,
         'Covers difficult situations you encounter while climbing, jumping, or swimming.'],
        ['Deception', 'CHA', False, 0, 0,
         'Determines whether you can convincingly hide the truth, either verbally or through your actions. This deception can encompass everything from misleading others through ambiguity to telling outright lies. Typical situations include trying to fast-talk a guard, con a merchant, earn money through gambling, pass yourself off in a disguise, dull someone’s suspicions with false assurances, or maintain a straight face while telling a blatant lie.'],
        ['History', 'INT', False, 0, 0,
         'Measures your ability to recall lore about historical events, legendary people, ancient kingdoms, past disputes, recent wars, and lost civilizations.'],
        ['Insight', 'WIS', False, 0, 0,
         'Decides whether you can determine the true intentions of a creature, such as when searching out a lie or predicting someone’s next move. Doing so involves gleaning clues from body language, speech habits, and changes in mannerisms.'],
        ['Intimidation', 'CHA', False, 0, 0,
         'When you attempt to influence someone through overt threats, hostile actions, and physical violence.'],
        ['Investigation', 'INT', False, 0, 0,
         'When you look around for clues and make deductions based on those clues'],
        ['Medicine', 'WIS', False, 0, 0,
         'Lets you try to stabilize a dying companion or diagnose an illness.'],
        ['Nature', 'INT', False, 0, 0,
         'Measures your ability to recall lore about terrain, plants and animals, the weather, and natural cycles.'],
        ['Perception', 'WIS', False, 0, 0,
         'Lets you spot, hear, or otherwise detect the presence of something. It measures your general awareness of your surroundings and the keenness of your senses.'],
        ['Performance', 'CHA', False, 0, 0,
         'Determines how well you can delight an audience with music, dance, acting, storytelling, or some other form of entertainment.'],
        ['Persuasion', 'CHA', False, 0, 0,
         'When you attempt to influence someone or a group of people with tact, social graces, or good nature'],
        ['Religion', 'INT', False, 0, 0,
         'Measures your ability to recall lore about deities, rites and prayers, religious hierarchies, holy symbols, and the practices of secret cults.'],
        ['Sleight of Hand', 'DEX', False, 0, 0,
         'Whenever you attempt an act of legerdemain or manual trickery, such as planting something on someone else or concealing an object on your person also check to determine whether you can lift a coin purse off another person or slip something out of another person’s pocket.'],
        ['Stealth', 'DEX', False, 0, 0,
         'When you attempt to conceal yourself from enemies, slink past guards, slip away without being noticed, or sneak up on someone without being seen or heard.'],
        ['Survival', 'WIS', False, 0, 0,
         'To follow tracks, hunt wild game, guide your group through frozen wastelands, identify signs that owlbears live nearby, predict the weather, or avoid quicksand and other natural hazards.']
        ],
        'Macros': [],
        'Money':[0,0,0,0],
        'Adventure Entries': []
        }
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = TCMT()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()