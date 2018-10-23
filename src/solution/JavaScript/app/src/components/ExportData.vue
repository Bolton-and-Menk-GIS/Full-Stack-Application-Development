<template>
  <b-modal id="export-modal"
           title="Export Data"
           header-text-variant="secondary"
           body-text-variant="secondary"
           :hide-footer="true"
           ref="exportModal"
           @ok="exportData">
    <b-card class="export-body">

      <div class="default" v-if="state === 'default'">
        <b-form-select v-model="selectedTable" :options="exportTables" class="mt-3 mb-3" />
        <b-form-group label="Export Format" v-if="selectedTable === 'breweries'" label-class="bold mt-2">
          <b-form-radio-group v-model="selectedExportType" :options="exportOptions" />
        </b-form-group>

        <div class="mx-auto mt-4">
          <b-button variant="danger" class="mr-4" style="font-weight: bold;" @click="dismiss">Cancel</b-button>
          <b-button class="theme" @click="exportData" :disabled="!selectedTable">Export Data</b-button>
        </div>
      </div>

      <spinner :visible="state === 'exporting'" text="Exporting Data..."/>

      <div class="download" v-if="state === 'completed'">
        <h4 class="theme">Successfully Exported <span class="capitalize">{{ selectedTable }}</span></h4>
        <font-awesome-icon
                title="download data"
                prefix="fas"
                icon="download"
                @click="download"
                class="download-btn mt-4">
        </font-awesome-icon>
      </div>

    </b-card>

  </b-modal>
</template>

<script>
  import api from '../modules/api';

  export default {
    name: "export-data",
    data() {
      return {
        state: 'default',
        downloadUrl: null,
        downloadFilename: null,
        selectedTable: null,
        selectedExportType: 'csv',
        exportTables: [
          { value: null, text: 'Select table to export' },
          { value: 'breweries', text: 'Breweries' },
          { value: 'beers', text: 'Beers' },
          { value: 'styles', text: 'Beer Styles' },
          { value: 'categories', text: 'Beer Categories' }
        ],
        exportOptions: [
          { value: 'csv', text: 'CSV' },
          { value: 'shapefile', text: 'Shapefile' }
        ]
      }
    },
    methods: {
      async exportData(){
        this.state = 'exporting';
        try {
          const result = await api.exportData({
            table: this.selectedTable,
            format: this.selectedExportType
          });
          this.url = result.url;
          this.filename = result.filename;
          this.state = 'completed';
        } catch(err){
          this.state = 'error';
        }

      },

      download(){
        const link = document.createElement('a');
        link.setAttribute('href', this.url);
        link.setAttribute('target', '_blank');
        link.setAttribute('download', this.filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        this.state = 'default';
      },

      dismiss(){
        this.$refs.exportModal.hide();
      }
    }
  }
</script>

<style scoped>

  .download-btn {
    color: forestgreen;
    font-size: 2.5rem;
    cursor: pointer;
  }
  .export-body {
    min-height: 250px;
    padding: 1.5rem;
    background-color: whitesmoke;
  }

</style>