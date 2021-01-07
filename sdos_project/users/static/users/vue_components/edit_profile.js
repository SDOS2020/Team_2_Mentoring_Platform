const EditProfile = {
	delimiters: ["[[", "]]"],
	template: `
		<div>
			[[ educations ]]
		</div>
	`,

	data () {
		return {
			educations: [],
			education: '',
		}
	},
	created () {
		return this.get_education()
	},
	methods : {
		get_education() {
			let request_url = "http://127.0.0.1:8000/api/get_education/";

			axios.get(request_url)
			.then(response => {
				console.log("[SUCCESS]");
				this.educations = response.data['educations'];
				console.log(this.educations);
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
				this.educations = [];
			});
		}
	}
}