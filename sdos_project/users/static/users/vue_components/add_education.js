const AddEducation = {
	delimiters: ["[[", "]]"],
	template: `
		<div>
			Education
			<a
				class="btn btn-sm btn-primary"
				data-toggle="modal"
				data-target="#addEduModalLong"
				style="float: right;"
			>
				Add More
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
							<h5>Qualification</h5>
							<input v-model="qualification" style="width: 100%;">
							</div>
							
							<div class="modal-body">
							<h5>Start Date</h5>
							<input v-model="start_date" type="date" required>
							</div>
							
						<div class="modal-body">
						<h5>End Date</h5>
							<input v-model="end_date" type="date" required>
							</div>
							
							<div class="modal-body">
							<h5>Organization</h5>
							<input v-model="organization" style="width: 100%;">
						</div>

						<div class="modal-body">
							<h5>Detail</h5>
							<textarea v-model="detail" style="width: 100%;"></textarea>
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

			<table class="table table-hover table-light table-sm">
				<tr v-for="(_, i) in qualifications.length" :key="i">
					<td>
						<b> [[ qualifications[i] ]] </b>
						<br/>
						<i> [[ start_dates[i] ]] - [[ end_dates[i] ]] </i>
						<br/>
						<b> [[ organizations[i] ]] </b>
						<br/>
						[[ details[i] ]]
						<hr>
					</td>
				</tr>
			</table>
		</div>
	`,

	data () {
		return {
			qualifications: [],
			start_dates: [],
			end_dates: [],
			organizations: [],
			details: [],
			
			qualification: '',
			start_date: '',
			end_date: '',
			organization: '',
			detail: '',
		}
	},
	created () {
		this.get_education();
	},
	methods : {
		get_education() {
			let request_url = "http://127.0.0.1:8000/api/get_education/";

			axios.get(request_url)
			.then(response => {
				console.log("[SUCCESS]");
				this.qualifications = response.data['qualifications'];
				this.start_dates = response.data['start_dates'];
				this.end_dates = response.data['end_dates'];
				this.organizations = response.data['organizations'];
				this.details = response.data['details'];
				console.log(this.qualifications);
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
				this.qualifications = [];
				this.start_dates = [];
				this.end_dates = [];
				this.organizations = [];
				this.details = [];
			});
		},

		add_education() {
			let request_url = "http://127.0.0.1:8000/api/add_education/";

			axios.get(request_url, {
				'params' : {
					'qualification': this.qualification,
					'start_date': this.start_date,
					'end_date': this.end_date,
					'organization': this.organization,
					'detail': this.detail,
				}
			})
			.then(response => {
				console.log("[SUCCESS]");
				this.get_education();
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});
			
			$('#addEduModalLong').modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
			
			this.qualification = '';
			this.start_date = '';
			this.end_date = '';
			this.organization = '';
			this.detail = '';
		},
	}
}