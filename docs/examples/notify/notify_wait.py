import npyscreen


class NotifyWaitExample(npyscreen.Form):
    def create(self):
        key_of_choice = 'p'
        what_to_display = 'Press {} for popup \n Press escape key to quit'.format(key_of_choice)

        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.exit_application
        self.add_handlers({key_of_choice: self.spawn_notify_popup})
        self.add(npyscreen.FixedText, value=what_to_display)

    def spawn_notify_popup(self, code_of_key_pressed):
        message_to_display = 'I popped up \n passed: {}'.format(code_of_key_pressed)
        npyscreen.notify_wait(message_to_display, title='Popup Title')

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', NotifyWaitExample, name='To show off notify_wait')


if __name__ == '__main__':
    TestApp = MyApplication().run()