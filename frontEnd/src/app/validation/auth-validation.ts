export class AuthValidation{
    // Creating array for storing errors.
    public errors:any = [];

    // create public function.
    public registerValidator(data:any):any{
        // Field must be valid a email.
        if(data.controls.email.errors == null){
            this.errors['email'] = '';
        }else{
            if(data.controls.email.errors.required){
                this.errors['email'] = 'This field is required.';
            }else{
                this.errors['email'] = '';
            }
        }

        // Password validation.
        if(data.controls.userPass.errors == null){
            this.errors['password'] = '';
        }else{
            if(data.controls.userPass.errors.required){
                this.errors['password'] = 'Password field is required.';
            } else if(data.controls.userPass.errors.minlength){
                this.errors['password'] = 'Password field must be more than 8 letters.';
            }else{
                this.errors['password'] = '';
            }
        }
        
        return this.errors;
    }
}