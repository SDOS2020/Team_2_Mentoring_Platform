const EditProfile = {
	delimiters: ["[[", "]]"],
	template: `
		<div>
			Education
			<a
				class="btn btn-sm btn-primary"
				data-toggle="modal"
				data-target="#addEduModalLong"
			>
				Add Education
			</a>

			<!-- START MODAL - addEduModal -->
			<div class="modal fade" id="addEduModalLong" tabindex="-1" role="dialog" aria-labelledby="addEduModalLongTitle" aria-hidden="true">
				<div class="modal-dialog" role="document">
					<div class="modal-content">
						<div class="modal-header">
							<h5 class="modal-title" id="addEduModalLongTitle">Add Education</h5>
							<button type="button" class="close" data-dismiss="modal" aria-label="Close">
								<span aria-hidden="true">&times;</span>
							</button>
						</div>
						
						<div class="modal-body">
							<h5>Enter details of your education</h5>
							<textarea v-model="education" style="width: 100%;"></textarea>
						</div>
						
						<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
							<button
								v-on:click="add_education()"
								type="button"
								class="btn btn-success"
							>
								Add
							</button>
						</div>
					</div>
				</div>
			</div>
			<!-- END MODAL -->

			<table class="table table-hover">

				<tbody>
					<tr v-for="(edu, index) in educations">
						<td>
							[[ edu ]]
						</td>
					</tr>
				</tbody>

			</table>
		</div>
	`,

	data () {
		return {
			educations: [],
			education: '',
			research_experiences: [],
			research_experience: '',
		}
	},
	created () {
		this.get_education();
		this.get_research_experience();
		return ;
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
		},
		add_education() {
			if (this.education.length < 10) {
				alert('[INFO] More info needed');
				return ;
			}
			if (this.education.length > 511) {
				alert('[ERROR] Please reduce the information');
				return ;
			}

			let request_url = "http://127.0.0.1:8000/api/add_education/";

			axios.get(request_url, {
				'params' : {
					'education' : this.education,
				}
			})
			.then(response => {
				console.log("[SUCCESS]");
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});
			
			$('#addEduModalLong').modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
			
			this.education = '';
			this.get_education();
		},
		
		get_research_experience() {
			let request_url = "http://127.0.0.1:8000/api/get_research_experience/";

			axios.get(request_url)
			.then(response => {
				console.log("[SUCCESS]");
				this.research_experiences = response.data['research_experiences'];
				console.log(this.research_experiences);
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
				this.research_experiences = [];
			});
		},
		add_research_experience() {
			if (this.research_experience.length < 10) {
				alert('[INFO] More info needed');
				return ;
			}
			if (this.research_experience.length > 511) {
				alert('[ERROR] Please reduce the information');
				return ;
			}

			let request_url = "http://127.0.0.1:8000/api/add_research_experience/";

			axios.get(request_url, {
				'params' : {
					'research_experience' : this.research_experience,
				}
			})
			.then(response => {
				console.log("[SUCCESS]");
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});
			
			$('#addEduModalLong').modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
			
			this.research_experience = '';
			this.get_research_experience();
		}
	}
}