

let time_remaining = JSON.parse(document.getElementById('time_remaining').textContent);

var app = new Vue({
    delimiters: ["[[", "]]"],
    el: '#quiz-app',
    data: {
        time_remaining: parseInt(time_remaining),
        formated_date: moment.utc(time_remaining*1000).format('HH:mm:ss')
    },
    methods: {
        countDown(){
            if (this.time_remaining > 0) {
                setTimeout( () => {
                    this.formated_date = moment.utc(this.time_remaining*1000).format('HH:mm:ss');
                    this.time_remaining--;
                    this.countDown();
                
                },1000)
            }
            else{
                formated_date = ""
          
                this.$refs.vue_submit.click()
             
            }
        }
    }, 
    created(){
        this.countDown();
    }
  })